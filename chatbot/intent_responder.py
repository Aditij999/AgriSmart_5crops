"""
Template-based responses for the Smart Agri chatbot's "intent" fast path.

This is a rewrite of the original chatbot/response_engine.py, adapted to the
report dict that app.py / backend/services/prediction_service.py assembles
(crop recommendation, soil status, fertilizer plan, yield prediction) rather
than the report_*.json files the old CLI chatbot read from disk. Every field
is read defensively with .get(), since demo/fallback data won't always have
every key that the full ML pipeline produces.

Multilingual support (English / Hindi / Marathi) is layered on top via
chatbot/language.py (script + keyword based language detection) and
chatbot/i18n.py (translated message templates and crop/nutrient/status
names). The caller (chatbot/router.py) may pass an explicit `lang`
("en"/"hi"/"mr"/"auto"/None); when it isn't a forced supported language,
the reply language is detected from the user's own message, so someone
typing in Hindi or Marathi gets a Hindi or Marathi answer even on their
first message.

Used by chatbot/router.py as the first thing tried for a user message; if no
handler matches (or the intent classifier wasn't confident enough), the
caller falls back to chatbot/gemini_chat.py.
"""

from chatbot.language import crop_role_from_message, extract_mentioned_crop, resolve_language
from chatbot.i18n import crop_name, fert_phrase, format_crop_list, msg, nutrient_name, status_name

SUPPORTED_CROPS = ["Jowar", "Groundnut", "Cotton", "Sugarcane", "Wheat"]

NUTRIENT_INTENTS = {
    "SOIL_NITROGEN": "Nitrogen",
    "SOIL_PHOSPHORUS": "Phosphorus",
    "SOIL_POTASSIUM": "Potassium",
    "SOIL_PH": "pH",
}

# Yield thresholds (kg/ha) mirror modules/yield_model.py's predict_yield().
YIELD_EMOJI = {
    "YIELD_LOW": "⚠️ ",
    "YIELD_MOD": "🟡 ",
    "YIELD_GOOD": "🟢 ",
    "YIELD_HIGH": "🟢 ",
}

# Intents that should never trigger a template — always handed to Gemini
# (or refused outright), because a canned line can't really do them justice.
NO_TEMPLATE_INTENTS = {"OUT_OF_SCOPE", "UNKNOWN"}


def _fmt(value, digits=1):
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def _recommended_crop(report):
    if report.get("recommended_crop"):
        return report["recommended_crop"]
    top5 = report.get("top_5_crops") or []
    if top5:
        return top5[0].get("crop")
    return None


def _yield_for_crop(report, crop):
    if not crop:
        return None
    by_crop = report.get("yields_by_crop") or {}
    if crop in by_crop:
        value = by_crop[crop]
        if isinstance(value, dict):
            return value.get("predicted_yield_kg_ha")
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    yield_info = report.get("yield_prediction") or {}
    nested = yield_info.get("yields_by_crop") or {}
    if crop in nested:
        try:
            return float(nested[crop])
        except (TypeError, ValueError):
            return None
    if crop == yield_info.get("recommended_crop"):
        raw = yield_info.get("recommended_crop_yield_kg_ha")
        try:
            return float(raw)
        except (TypeError, ValueError):
            pass
    if crop == (yield_info.get("crop") or report.get("chosen_crop")):
        raw = yield_info.get("predicted_yield_kg_ha")
        try:
            return float(raw)
        except (TypeError, ValueError):
            return None
    return None


def _calculate_yield_now(report, crop):
    """Run the existing yield model for `crop` from this analysis's soil readings.

    Returns kg/ha or None. Only supported crops are calculated (see
    prediction_service.predict_yield_for_crop); nothing is invented.
    """
    soil = report.get("soil_input") or {}
    if not soil:
        return None
    try:
        from backend.services.prediction_service import predict_yield_for_crop
        return predict_yield_for_crop(soil, crop)
    except Exception:
        return None


def _yield_answer_for_crop(report, crop, lang, prefix=""):
    """Answer for exactly `crop`: saved value -> newly calculated -> unavailable."""
    saved = _yield_for_crop(report, crop)
    if saved is not None:
        return prefix + msg(lang, "YIELD_SAVED", crop=crop_name(crop, lang),
                            yield_kg=saved, yield_t=saved / 1000.0)
    calculated = _calculate_yield_now(report, crop)
    if calculated is not None:
        return prefix + msg(lang, "YIELD_CALCULATED", crop=crop_name(crop, lang),
                            yield_kg=calculated, yield_t=calculated / 1000.0)
    return msg(lang, "YIELD_NOT_POSSIBLE", crop=crop_name(crop, lang),
               crops=format_crop_list(SUPPORTED_CROPS, lang))


def _recommended_fertilizer_block(report, lang):
    """Fertilizer advice computed for the RECOMMENDED crop (separate from target)."""
    recommended = _recommended_crop(report)
    if not recommended:
        return None
    info = (report.get("fertilizer") or {}).get("recommended_crop_fertilizer")
    if not info or not info.get("available"):
        return msg(lang, "FERT_REC_UNAVAILABLE", crop=crop_name(recommended, lang))
    recs = (info.get("result") or {}).get("generic_recs") or []
    if not recs:
        return msg(lang, "FERTILIZER_BALANCED", prefix="", crop=crop_name(recommended, lang))
    lines = [msg(lang, "FERT_REC_HEADER", crop=crop_name(recommended, lang))]
    for rec in recs:
        lines.append(msg(lang, "FERTILIZER_DOSAGE_LINE", label=rec.get("fertilizer"),
                         dose=fert_phrase(rec.get("dose_note"), lang)))
    return "\n".join(lines)


def _nutrient_unit(nutrient):
    return "" if nutrient == "pH" else " kg/ha"


def _soil_action(lang, status, crop):
    if status == "Low":
        return msg(lang, "SOIL_ACTION_LOW", crop=crop_name(crop, lang) if crop else "")
    if status == "High":
        return msg(lang, "SOIL_ACTION_HIGH")
    return msg(lang, "SOIL_ACTION_OK")


def _yield_interp_key(predicted_yield_kg_ha):
    try:
        pred = float(predicted_yield_kg_ha)
    except (TypeError, ValueError):
        return None
    if pred < 1000:
        return "YIELD_LOW"
    if pred < 3000:
        return "YIELD_MOD"
    if pred < 15000:
        return "YIELD_GOOD"
    return "YIELD_HIGH"


def generate_response(intent, report, user_message="", lang=None):
    """
    Return a canned answer for `intent` using `report`, or None if this
    intent isn't one the template engine handles (caller should fall back
    to the Gemini API in that case).

    `lang` may be "en" / "hi" / "mr" / "auto" / None. When it isn't a
    forced supported language, the reply language is detected from
    `user_message` (Devanagari script + Hindi/Marathi marker words).
    """
    report = report or {}
    lang = resolve_language(user_message, preferred=lang)
    target_crop = report.get("chosen_crop")
    recommended = _recommended_crop(report)
    grown_crop = report.get("grown_crop")
    mentioned = extract_mentioned_crop(user_message)
    role = crop_role_from_message(user_message)
    if mentioned:
        crop = mentioned
        override_prefix = ""
        if mentioned != target_crop and mentioned != recommended:
            override_prefix = msg(
                lang, "OVERRIDE_PREFIX",
                chosen=crop_name(recommended or target_crop, lang),
                crop=crop_name(mentioned, lang),
            )
        elif mentioned != target_crop:
            override_prefix = ""
    elif role == "recommended":
        crop = recommended
        override_prefix = ""
    elif role == "grown":
        crop = grown_crop
        override_prefix = ""
    else:
        crop = target_crop
        override_prefix = ""

    # ---- Small talk / meta ---------------------------------------------
    if intent == "GREETING":
        return msg(lang, "GREETING")

    if intent == "HELP":
        return msg(lang, "HELP")

    if intent == "SYSTEM_OVERVIEW":
        return msg(lang, "SYSTEM_OVERVIEW")

    if intent == "HOW_TO_USE":
        return msg(lang, "HOW_TO_USE")

    if intent == "DASHBOARD":
        return msg(lang, "DASHBOARD")

    if intent == "ML_MODEL_EXPLANATION":
        return msg(lang, "ML_MODEL_EXPLANATION")

    if intent == "SUPPORTED_CROPS":
        return msg(lang, "SUPPORTED_CROPS", crops=format_crop_list(SUPPORTED_CROPS, lang))

    # ---- Crop recommendation --------------------------------------------
    if intent == "CROP_RECOMMENDATION":
        if not recommended:
            return None
        return msg(lang, "CROP_RECOMMENDATION", crop=crop_name(recommended, lang))

    if intent == "CROP_RECOMMENDATION_EXPLANATION":
        top5 = report.get("top_5_crops") or []
        if not top5:
            return None
        top = top5[0]
        probability = (top.get("probability") or 0) * 100
        return msg(
            lang,
            "CROP_RECOMMENDATION_EXPLANATION",
            crop=crop_name(top.get("crop", crop), lang),
            probability=probability,
        )

    if intent == "CROP_PROBABILITY":
        top5 = report.get("top_5_crops") or []
        if not top5:
            return None
        lines = [msg(lang, "CROP_PROBABILITY_HEADER")]
        for item in top5:
            probability = (item.get("probability") or 0) * 100
            lines.append(
                msg(
                    lang,
                    "CROP_PROBABILITY_LINE",
                    crop=crop_name(item.get("crop"), lang),
                    probability=probability,
                )
            )
        return "\n".join(lines)

    if intent == "CROP_SOIL_MISMATCH":
        top5 = report.get("top_5_crops") or []
        compare_crop = mentioned or target_crop
        if not top5 or not compare_crop:
            return None
        top_crop = top5[0].get("crop")
        if top_crop and top_crop != compare_crop:
            return msg(
                lang,
                "CROP_MISMATCH_BETTER",
                top_crop=crop_name(top_crop, lang),
                crop=crop_name(compare_crop, lang),
            )
        return msg(lang, "CROP_MISMATCH_BEST", crop=crop_name(compare_crop, lang))

    # ---- Soil -------------------------------------------------------------
    if intent == "SOIL_ANALYSIS":
        soil_adjustment = report.get("soil_adjustment") or {}
        soil_crop = target_crop
        if not soil_adjustment:
            soil = report.get("soil_input")
            if not soil:
                return None
            return msg(
                lang,
                "SOIL_ANALYSIS",
                crop=crop_name(soil_crop, lang) if soil_crop else "",
                lines="\n".join(
                    f"• {key}: {value}" for key, value in soil.items()
                ),
            )
        lines = []
        imbalances = []
        for nutrient, info in soil_adjustment.items():
            unit = _nutrient_unit(nutrient)
            status = info.get("status")
            line = msg(
                lang,
                "SOIL_ANALYSIS_LINE",
                nutrient=nutrient_name(nutrient, lang),
                current=info.get("current"),
                unit=unit,
                status=status_name(status, lang),
                ideal=info.get("ideal"),
            )
            lines.append(line)
            if status and status != "Optimal":
                imbalances.append((nutrient, info))
        body = msg(
            lang,
            "SOIL_ANALYSIS",
            crop=crop_name(soil_crop, lang) if soil_crop else "",
            lines="\n".join(lines),
        )
        if imbalances:
            extra = [msg(
                lang, "SOIL_IMBALANCE_HEADER",
                count=len(imbalances),
                crop=crop_name(soil_crop, lang) if soil_crop else "",
            )]
            for nutrient, info in imbalances:
                extra.append(msg(
                    lang,
                    "SOIL_IMBALANCE_LINE",
                    nutrient=nutrient_name(nutrient, lang),
                    current=info.get("current"),
                    unit=_nutrient_unit(nutrient),
                    status=status_name(info.get("status"), lang),
                    ideal=info.get("ideal"),
                    action=_soil_action(lang, info.get("status"), soil_crop),
                ))
            return body + "\n\n" + "\n".join(extra)
        return body + "\n\n" + msg(lang, "SOIL_ALL_OPTIMAL", crop=crop_name(soil_crop, lang) if soil_crop else "")

    if intent in NUTRIENT_INTENTS:
        nutrient = NUTRIENT_INTENTS[intent]
        soil_adjustment = report.get("soil_adjustment") or {}
        unit = "" if nutrient == "pH" else " kg/ha"

        if nutrient not in soil_adjustment:
            current_value = (report.get("soil_input") or {}).get(nutrient)
            if current_value is None or not target_crop:
                return None
            return msg(
                lang,
                "NUTRIENT_NO_ADJUSTMENT",
                nutrient=nutrient_name(nutrient, lang),
                value=current_value,
                unit=unit,
                crop=crop_name(target_crop, lang),
            )

        info = soil_adjustment[nutrient]
        return msg(
            lang,
            "NUTRIENT_STATUS",
            prefix="",
            nutrient=nutrient_name(nutrient, lang),
            current=info.get("current"),
            unit=unit,
            crop=crop_name(target_crop, lang) if target_crop else "",
            ideal=info.get("ideal"),
            status=status_name(info.get("status"), lang),
        )

    if intent == "SOIL_STATUS_EXPLANATION":
        soil_adjustment = report.get("soil_adjustment") or {}
        explanation = msg(lang, "SOIL_STATUS_EXPLANATION")
        if not soil_adjustment:
            return explanation
        imbalances = [
            (nutrient, info)
            for nutrient, info in soil_adjustment.items()
            if info.get("status") and info.get("status") != "Optimal"
        ]
        if not imbalances:
            return explanation + "\n\n" + msg(
                lang, "SOIL_ALL_OPTIMAL",
                crop=crop_name(target_crop, lang) if target_crop else "",
            )
        extra = [msg(
            lang, "SOIL_IMBALANCE_HEADER",
            count=len(imbalances),
            crop=crop_name(target_crop, lang) if target_crop else "",
        )]
        for nutrient, info in imbalances:
            extra.append(msg(
                lang,
                "SOIL_IMBALANCE_LINE",
                nutrient=nutrient_name(nutrient, lang),
                current=info.get("current"),
                unit=_nutrient_unit(nutrient),
                status=status_name(info.get("status"), lang),
                ideal=info.get("ideal"),
                action=_soil_action(lang, info.get("status"), target_crop),
            ))
        return explanation + "\n\n" + "\n".join(extra)

    # ---- Fertilizer ---------------------------------------------------
    fertilizer = report.get("fertilizer") or {}
    recs = fertilizer.get("generic_recs") or []

    if intent == "FERTILIZER_RECOMMENDATION":
        if (mentioned and mentioned == recommended and mentioned != target_crop) or role == "recommended":
            return _recommended_fertilizer_block(report, lang)
        if mentioned and target_crop and mentioned != target_crop:
            return msg(
                lang, "FERTILIZER_OTHER_CROP",
                target=crop_name(target_crop, lang),
                crop=crop_name(mentioned, lang),
            )
        if not fertilizer:
            return None
        if not fertilizer.get("action_needed", bool(recs)):
            return msg(lang, "FERTILIZER_BALANCED", prefix="", crop=crop_name(crop, lang) if crop else "")
        lines = [msg(lang, "FERTILIZER_BASED", prefix="")]
        for rec in recs:
            lines.append(
                msg(
                    lang,
                    "FERTILIZER_CONDITION_LINE",
                    nutrient=nutrient_name(rec.get("nutrient"), lang),
                    status=status_name(rec.get("condition"), lang),
                    label=rec.get("fertilizer"),
                )
            )
        crop_primary = fertilizer.get("crop_primary")
        if crop_primary:
            lines.append(
                msg(
                    lang,
                    "FERTILIZER_PRIMARY",
                    crop=crop_name(crop, lang) if crop else "",
                    fertilizer=crop_primary.get("fertilizer"),
                )
            )
        return "\n".join(lines)

    if intent == "FERTILIZER_DOSAGE":
        if (mentioned and mentioned == recommended and mentioned != target_crop) or role == "recommended":
            return _recommended_fertilizer_block(report, lang)
        if mentioned and target_crop and mentioned != target_crop:
            return msg(
                lang, "FERTILIZER_OTHER_CROP",
                target=crop_name(target_crop, lang),
                crop=crop_name(mentioned, lang),
            )
        if not recs:
            return msg(lang, "FERTILIZER_DOSAGE_NONE", prefix="", crop=crop_name(crop, lang) if crop else "")
        lines = [msg(lang, "FERTILIZER_DOSAGE_HEADER", prefix="")]
        for rec in recs:
            lines.append(
                msg(
                    lang,
                    "FERTILIZER_DOSAGE_LINE",
                    label=rec.get("fertilizer"),
                    dose=fert_phrase(rec.get("dose_note"), lang),
                )
            )
        return "\n".join(lines)

    if intent == "WHY_FERTILIZER_NEEDED":
        if not recs:
            return msg(lang, "WHY_FERT_NONE", prefix="", crop=crop_name(crop, lang) if crop else "")
        lines = [msg(lang, "WHY_FERT_HEADER", prefix="")]
        for rec in recs:
            lines.append(
                msg(
                    lang,
                    "WHY_FERT_LINE",
                    label=rec.get("fertilizer"),
                    reason=fert_phrase(rec.get("reason"), lang),
                )
            )
        return "\n".join(lines)

    if intent == "FERTILIZER_EXPLANATION":
        if not recs:
            return msg(lang, "FERT_EXPLAIN_NONE", prefix="", crop=crop_name(crop, lang) if crop else "")
        lines = [msg(lang, "FERT_EXPLAIN_HEADER", prefix="")]
        for rec in recs:
            lines.append(
                msg(
                    lang,
                    "FERT_EXPLAIN_LINE",
                    label=rec.get("fertilizer"),
                    npk=rec.get("npk_ratio"),
                    reason=fert_phrase(rec.get("reason"), lang),
                )
            )
        return "\n".join(lines)

    # ---- Yield --------------------------------------------------------
    yield_info = report.get("yield_prediction") or {}

    if intent == "YIELD_PREDICTION":
        if mentioned:
            return _yield_answer_for_crop(report, mentioned, lang, override_prefix)
        if role == "recommended":
            if not recommended:
                return msg(lang, "YIELD_NOT_POSSIBLE", crop="", crops=format_crop_list(SUPPORTED_CROPS, lang))
            return _yield_answer_for_crop(report, recommended, lang)
        if role == "grown":
            if not grown_crop:
                return None
            return _yield_answer_for_crop(report, grown_crop, lang)
        target_yield = _yield_for_crop(report, target_crop)
        rec_yield = _yield_for_crop(report, recommended)
        if (
            target_crop and recommended and target_crop != recommended
            and target_yield is not None and rec_yield is not None
        ):
            return msg(
                lang, "YIELD_PREDICTION_BOTH",
                target=crop_name(target_crop, lang),
                target_yield=target_yield,
                recommended=crop_name(recommended, lang),
                recommended_yield=rec_yield,
            )
        if target_yield is None or not target_crop:
            return None
        return msg(
            lang, "YIELD_PREDICTION",
            prefix="",
            crop=crop_name(target_crop, lang),
            yield_kg=target_yield,
        )

    if intent == "YIELD_EXPLANATION":
        interp_key = _yield_interp_key(yield_info.get("predicted_yield_kg_ha"))
        if not interp_key:
            return yield_info.get("interpretation")
        return YIELD_EMOJI.get(interp_key, "") + msg(lang, interp_key)

    if intent == "YIELD_FACTORS":
        return msg(lang, "YIELD_FACTORS")

    if intent == "YIELD_STATUS_EXPLANATION":
        return msg(lang, "YIELD_STATUS_EXPLANATION")

    # No template for this intent (includes OUT_OF_SCOPE / UNKNOWN).
    return None
