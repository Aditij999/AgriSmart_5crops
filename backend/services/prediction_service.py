"""Thin adapter around the existing ML pipeline.

Nothing here re-implements or re-trains anything: `pipeline.run_pipeline` is
the same entry point the Streamlit app's modules use, and it already chains
crop recommendation -> soil adjustment -> fertilizer rules -> yield model.
This module only converts between the API's JSON shapes and the pipeline's
dicts, and silences the pipeline's console report.
"""

import contextlib
import io
import os
import sys
from typing import Any

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.fertilizer_recommendation import recommend_fertilizer  # noqa: E402
from modules.soil_adjustment import get_supported_crops  # noqa: E402
from modules.yield_model import load_model as load_yield_model  # noqa: E402
from modules.yield_model import predict_yield  # noqa: E402
from pipeline import run_pipeline  # noqa: E402

FIELD_TO_PIPELINE_KEY = {
    "nitrogen": "Nitrogen",
    "phosphorus": "Phosphorus",
    "potassium": "Potassium",
    "ph": "pH",
    "temperature": "Temperature",
    "rainfall": "Rainfall",
}

UNITS = {
    "nitrogen": "kg/ha",
    "phosphorus": "kg/ha",
    "potassium": "kg/ha",
    "ph": "",
    "temperature": "°C",
    "rainfall": "mm",
}

# Match-score bands are applied to the crop model's probability as a
# percentage (0–100) among the five supported crops.
MATCH_HIGH_PCT = 40.0
MATCH_MODERATE_PCT = 25.0


def supported_crops() -> list[str]:
    return get_supported_crops()


def probability_as_percent(probability: float | None) -> float | None:
    if probability is None:
        return None
    value = float(probability)
    return round(value * 100.0, 1) if value <= 1.0 else round(value, 1)


def match_label(probability: float | None) -> str:
    percent = probability_as_percent(probability)
    if percent is None:
        return "No score"
    if percent >= MATCH_HIGH_PCT:
        return "High Match"
    if percent >= MATCH_MODERATE_PCT:
        return "Moderate Match"
    return "Low Match"


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def _as_yield(raw: Any) -> float | None:
    return float(raw) if isinstance(raw, (int, float)) else None


# ---------------------------------------------------------------------------
# Units and shared yield / fertilizer helpers (single source of truth for the
# website dashboard, the API, History and the chatbot).
# ---------------------------------------------------------------------------
YIELD_BAND_FRACTION = 0.12  # indicative +/-12% band around the point estimate


def kg_ha_to_t_ha(kg_ha: float | None) -> float | None:
    if kg_ha is None:
        return None
    return round(float(kg_ha) / 1000.0, 3)


def t_ha_to_kg_ha(t_ha: float | None) -> float | None:
    if t_ha is None:
        return None
    return round(float(t_ha) * 1000.0, 1)


def yield_band_kg_ha(kg_ha: float | None) -> tuple[float, float] | None:
    """Indicative band around a point estimate (NOT a model confidence interval)."""
    if kg_ha is None or kg_ha < 0:
        return None
    return (round(kg_ha * (1 - YIELD_BAND_FRACTION), 1), round(kg_ha * (1 + YIELD_BAND_FRACTION), 1))


def to_pipeline_soil(soil: dict[str, float]) -> dict[str, float]:
    """Accept API-style (lowercase) or pipeline-style keys; return pipeline keys."""
    out: dict[str, float] = {}
    for field, key in FIELD_TO_PIPELINE_KEY.items():
        if key in soil:
            out[key] = float(soil[key])
        elif field in soil:
            out[key] = float(soil[field])
    return out


_REFERENCE_YIELDS: dict[str, float] | None = None


def reference_yield_kg_ha(crop: str | None) -> float | None:
    """Mean observed yield for `crop` in the dataset the yield model was trained on.

    Used only as the "typical yield" reference for comparisons; None when the
    dataset or crop is unavailable (callers then hide the comparison).
    """
    global _REFERENCE_YIELDS
    if _REFERENCE_YIELDS is None:
        _REFERENCE_YIELDS = {}
        try:
            import pandas as pd

            df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "merged_yield_dataset.csv"))
            _REFERENCE_YIELDS = {
                str(k): float(v) for k, v in df.groupby("Crop")["Yield_kg_ha"].mean().items()
            }
        except Exception:
            _REFERENCE_YIELDS = {}
    return _REFERENCE_YIELDS.get(crop) if crop else None


def is_supported_crop(crop: str | None) -> bool:
    return bool(crop) and crop in get_supported_crops()


def predict_yield_for_crop(soil: dict[str, float], crop: str | None) -> float | None:
    """Yield (kg/ha) from the existing yield model for ONE supported crop, else None.

    Unsupported crops return None on purpose: the model would otherwise fall
    back to a mean crop encoding and produce a number that belongs to no crop.
    """
    if not is_supported_crop(crop):
        return None
    try:
        result = predict_yield(to_pipeline_soil(soil), model=load_yield_model(), crop=crop)
    except (FileNotFoundError, KeyError):
        return None
    return _as_yield(result.get("predicted_yield_kg_ha"))


def fertilizer_for_crop(crop: str | None, soil: dict[str, float]) -> dict[str, Any]:
    """Run the existing fertilizer rules for exactly `crop`.

    Always returns {"crop", "available", "result", "reason"}; never raises for
    unsupported crops and never relabels another crop's result.
    """
    if not crop:
        return {"crop": None, "available": False, "result": None, "reason": "No crop given."}
    if not is_supported_crop(crop):
        return {
            "crop": crop,
            "available": False,
            "result": None,
            "reason": f"Fertilizer advice is not available for {crop}; supported crops are "
            f"{', '.join(get_supported_crops())}.",
        }
    pipeline_soil = to_pipeline_soil(soil)
    result = _to_jsonable(
        recommend_fertilizer(crop, {k: pipeline_soil[k] for k in ("Nitrogen", "Phosphorus", "Potassium", "pH")})
    )
    return {"crop": crop, "available": True, "result": result, "reason": None}


def run_analysis(soil: dict[str, float], crop: str | None = None) -> dict[str, Any]:
    """Run the full pipeline for one soil reading and return a JSON-safe report.

    Yield for the *target* crop (user selection / auto-selected recommendation)
    stays on `predicted_yield_kg_ha`. Yield for every supported crop, including
    the model-recommended crop, is stored separately so UI and chatbot never
    mix them up.
    """
    soil_input = {FIELD_TO_PIPELINE_KEY[field]: float(soil[field]) for field in FIELD_TO_PIPELINE_KEY}

    with contextlib.redirect_stdout(io.StringIO()):
        report = run_pipeline(soil_input, chosen_crop=crop)

    report = _to_jsonable(report)

    top_crops = [
        {"crop": item["crop"], "probability": float(item["probability"])}
        for item in report.get("top_5_crops", [])
    ]
    recommended_crop = top_crops[0]["crop"] if top_crops else None
    recommended_prob = top_crops[0]["probability"] if top_crops else None
    chosen_crop = report.get("chosen_crop")

    yield_prediction = dict(report.get("yield_prediction") or {})
    target_yield = _as_yield(yield_prediction.get("predicted_yield_kg_ha"))

    yields_by_crop: dict[str, float] = {}
    try:
        yield_model = load_yield_model()
        for crop_name in get_supported_crops():
            predicted = predict_yield(soil_input, model=yield_model, crop=crop_name)
            kg_ha = _as_yield(predicted.get("predicted_yield_kg_ha"))
            if kg_ha is not None:
                yields_by_crop[crop_name] = kg_ha
    except FileNotFoundError:
        if chosen_crop and target_yield is not None:
            yields_by_crop[chosen_crop] = target_yield

    if chosen_crop and target_yield is not None:
        yields_by_crop[chosen_crop] = target_yield

    recommended_yield = yields_by_crop.get(recommended_crop) if recommended_crop else None

    yield_prediction.update(
        {
            "crop": chosen_crop,
            "predicted_yield_kg_ha": target_yield,
            "unit": "kg/ha",
            "is_estimate": True,
            "recommended_crop": recommended_crop,
            "recommended_crop_yield_kg_ha": recommended_yield,
            "yields_by_crop": yields_by_crop,
        }
    )

    # Fertilizer for the TARGET crop stays as the pipeline produced it. The
    # recommended crop gets its own calculation, stored under an extra key so
    # old consumers of `fertilizer` keep working unchanged.
    fertilizer = dict(report.get("fertilizer") or {})
    fertilizer["recommended_crop_fertilizer"] = fertilizer_for_crop(recommended_crop, soil_input)

    return {
        "soil_input": {field: float(soil[field]) for field in FIELD_TO_PIPELINE_KEY},
        "chosen_crop": chosen_crop,
        "recommended_crop": recommended_crop,
        "recommended_crop_probability": recommended_prob,
        "predicted_yield_kg_ha": target_yield,
        "recommended_yield_kg_ha": recommended_yield,
        "yields_by_crop": yields_by_crop,
        "top_crops": top_crops,
        "soil_analysis": report.get("soil_adjustment") or {},
        "fertilizer": fertilizer,
        "yield_prediction": yield_prediction,
    }


def to_chatbot_report(entry: dict[str, Any]) -> dict[str, Any]:
    """Reshape a stored/returned prediction into the dict the chatbot expects."""
    yield_prediction = dict(entry.get("yield_prediction") or {})
    yields_by_crop = entry.get("yields_by_crop") or yield_prediction.get("yields_by_crop") or {}
    return {
        "chosen_crop": entry.get("chosen_crop"),
        "recommended_crop": entry.get("recommended_crop"),
        "grown_crop": entry.get("grown_crop"),
        "recommended_crop_probability": entry.get("recommended_crop_probability"),
        "top_5_crops": entry.get("top_crops") or [],
        "soil_input": {
            FIELD_TO_PIPELINE_KEY[field]: value
            for field, value in (entry.get("soil_input") or {}).items()
            if field in FIELD_TO_PIPELINE_KEY
        },
        "soil_adjustment": entry.get("soil_analysis") or {},
        "fertilizer": entry.get("fertilizer") or {},
        "yield_prediction": yield_prediction,
        "yields_by_crop": yields_by_crop,
        "predicted_yield_kg_ha": entry.get("predicted_yield_kg_ha"),
        "recommended_yield_kg_ha": entry.get("recommended_yield_kg_ha")
        or yield_prediction.get("recommended_crop_yield_kg_ha"),
    }
