"""Pure-logic tests: crop mapping, yield selection, units, fertilizer crop, chatbot."""
import copy
import pytest

from backend.services import prediction_service as ps
from chatbot.language import extract_mentioned_crop
from chatbot.router import answer_question

# Real soil for which the crop model's top class is Groundnut (verified against models/).
GROUNDNUT_SOIL = dict(nitrogen=27, phosphorus=82, potassium=18, ph=6.6, temperature=24, rainfall=460)


@pytest.fixture(scope="module")
def analysis():
    return ps.run_analysis(GROUNDNUT_SOIL, "Jowar")


def test_recommended_crop_is_model_output_not_target(analysis):
    assert analysis["recommended_crop"] == "Groundnut"
    assert analysis["chosen_crop"] == "Jowar"
    assert analysis["top_crops"][0]["crop"] == analysis["recommended_crop"]
    assert analysis["recommended_crop_probability"] == analysis["top_crops"][0]["probability"]


def test_yields_are_per_crop_and_distinct(analysis):
    y = analysis["yields_by_crop"]
    assert analysis["predicted_yield_kg_ha"] == y["Jowar"]
    assert analysis["recommended_yield_kg_ha"] == y["Groundnut"]
    assert set(y) == set(ps.supported_crops())


def test_fertilizer_for_recommended_crop_is_computed_for_that_crop(analysis):
    rec = analysis["fertilizer"]["recommended_crop_fertilizer"]
    assert rec["crop"] == "Groundnut" and rec["available"]
    direct = ps.fertilizer_for_crop("Groundnut", GROUNDNUT_SOIL)["result"]
    assert rec["result"]["generic_recs"] == direct["generic_recs"]
    # target-crop result is untouched and comes from the Jowar rules
    jowar = ps.fertilizer_for_crop("Jowar", GROUNDNUT_SOIL)["result"]
    assert analysis["fertilizer"]["generic_recs"] == jowar["generic_recs"]
    # ideal values differ per crop, proving it is not a relabelled copy
    assert rec["result"]["gap_analysis"] != jowar["gap_analysis"]


def test_fertilizer_unavailable_for_unsupported_crop():
    out = ps.fertilizer_for_crop("Turmeric", GROUNDNUT_SOIL)
    assert out["available"] is False and out["result"] is None and "Turmeric" in out["reason"]


def test_yield_never_invented_for_unsupported_crop():
    assert ps.predict_yield_for_crop(GROUNDNUT_SOIL, "Turmeric") is None
    assert ps.predict_yield_for_crop(GROUNDNUT_SOIL, None) is None


def test_unit_conversion_round_trip_and_band():
    assert ps.kg_ha_to_t_ha(1369.0) == 1.369
    assert ps.t_ha_to_kg_ha(ps.kg_ha_to_t_ha(17418.1)) == pytest.approx(17418.1, abs=0.5)
    lo, hi = ps.yield_band_kg_ha(1000)
    assert (lo, hi) == (880.0, 1120.0) and lo < 1000 < hi
    assert ps.yield_band_kg_ha(None) is None


def test_match_label_uses_fraction_not_percent_confusion():
    assert ps.match_label(0.576) == "High Match"
    assert ps.match_label(0.008) == "Low Match"      # 0.8 %, must not be read as 80 %
    assert ps.match_label(None) == "No score"


@pytest.mark.parametrize("text,crop", [
    ("उस्म्याच्या पिकाचे अपेक्षित उत्पादन किती आहे?", "Sugarcane"),
    ("ऊसाचे उत्पादन किती?", "Sugarcane"), ("गन्ने की पैदावार कितनी होगी", "Sugarcane"),
    ("what is the sugarcane yield", "Sugarcane"),
    ("गव्हाचे उत्पादन", "Wheat"), ("गेहूं की उपज", "Wheat"),
    ("कापसाचे उत्पादन", "Cotton"), ("ज्वारीच्या पिकाचे", "Jowar"),
    ("भुईमुगाच्या शेंगा", "Groundnut"), ("peanut yield", "Groundnut"),
    ("how is the weather", None),
])
def test_chatbot_crop_identification(text, crop):
    assert extract_mentioned_crop(text) == crop


MR_Q = "उस्म्याच्या पिकाचे अपेक्षित उत्पादन किती आहे?"


@pytest.fixture()
def report(analysis):
    return ps.to_chatbot_report(analysis)


def test_marathi_sugarcane_question_never_returns_wheat_or_target_yield(report):
    ans, _ = answer_question(MR_Q, report, [], "", "auto")
    y = report["yields_by_crop"]
    assert f"{y['Sugarcane']:,.1f}" in ans
    for other in ("Wheat", "Jowar", "Groundnut", "Cotton"):
        assert f"{y[other]:,.1f}" not in ans


def test_saved_vs_calculated_are_distinguished(report):
    saved, _ = answer_question(MR_Q, report, [], "", "mr")
    assert "साठवलेला अंदाज" in saved
    r2 = copy.deepcopy(report)
    r2["yields_by_crop"], r2["yield_prediction"] = {}, {}
    calc, _ = answer_question(MR_Q, r2, [], "", "mr")
    assert "आता तो काढला" in calc
    assert f"{report['yields_by_crop']['Sugarcane']:,.1f}" in calc   # same model value, same units


def test_sugarcane_unavailable_is_stated_without_a_number(report):
    r3 = copy.deepcopy(report)
    r3["yields_by_crop"], r3["yield_prediction"], r3["soil_input"] = {}, {}, {}
    ans, _ = answer_question(MR_Q, r3, [], "", "mr")
    assert "अद्याप अंदाजित केलेले नाही" in ans
    assert "kg/ha" not in ans


@pytest.mark.parametrize("q,lang,unit", [
    ("What is the expected yield of sugarcane?", "en", "kg/ha"),
    ("ऊस का उत्पादन कितना होगा?", "hi", "kg/ha"),
])
def test_chatbot_multilingual_yield(report, q, lang, unit):
    ans, src = answer_question(q, report, [], "", lang)
    assert src == "intent" and unit in ans
    assert f"{report['yields_by_crop']['Sugarcane']:,.1f}" in ans
