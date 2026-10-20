import os
import pytest
from streamlit.testing.v1 import AppTest

import web_voice
from backend.services import prediction_service as ps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _dash(target):
    at = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=150).run()
    at.selectbox[0].set_value(target)       # default sliders = the screenshot's soil
    at.button[0].click()
    return at.run()


def _fert_kpi(at):
    return [(m.label, m.value) for m in at.metric if m.label.startswith("🧪 Fertilizers")][0]


def _expected_count(crop):
    soil = dict(nitrogen=58, phosphorus=43, potassium=37, ph=6.4, temperature=26.5, rainfall=820)
    recs = ps.fertilizer_for_crop(crop, soil)["result"]["generic_recs"]
    return sum(1 for r in recs if r["condition"] == "Low")     # only "Low" rows carry a dose


def test_fertilizer_tile_matches_the_card_and_follows_the_switch():
    at = _dash("Cotton")
    assert not at.exception
    rec = ps.run_analysis(dict(nitrogen=58, phosphorus=43, potassium=37, ph=6.4, temperature=26.5, rainfall=820), "Cotton")["recommended_crop"]
    assert rec != "Cotton"
    label, value = _fert_kpi(at)
    assert label == f"🧪 Fertilizers ({rec})" and value == f"{_expected_count(rec)} to apply"
    assert f"Fertilizer — {rec}" in " ".join(m.value for m in at.markdown)
    [r for r in at.radio if r.label == "Fertilizer advice for"][0].set_value("Target crop")
    at.run()
    label, value = _fert_kpi(at)
    assert label == "🧪 Fertilizers (Cotton)" and value == f"{_expected_count('Cotton')} to apply"


@pytest.mark.parametrize("choice,tag", [("en", "en-IN"), ("hi", "hi-IN"), ("mr", "mr-IN"), ("auto", "en-IN"), (None, "en-IN")])
def test_mic_language_follows_chat_language(choice, tag):
    assert web_voice.speech_lang_for(choice) == tag


def test_read_aloud_voice_matches_text_language():
    assert web_voice.tts_lang_for_text("या विश्लेषणासाठी ऊस पिकाचे उत्पादन आहे") == "mr-IN"
    assert web_voice.tts_lang_for_text("आपकी फसल का उत्पादन कितना है") == "hi-IN"
    assert web_voice.tts_lang_for_text("Estimated yield is 17,418 kg/ha") == "en-IN"


def test_component_no_longer_hardcodes_english():
    html = open(os.path.join(ROOT, "web_voice_component", "index.html"), encoding="utf-8").read()
    assert "en-US" not in html and "recognizer.lang = currentLang" in html and "args.lang" in html
