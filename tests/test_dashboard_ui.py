"""Drives the real Streamlit app headlessly (streamlit.testing.AppTest)."""
import os
import re
import pytest
from streamlit.testing.v1 import AppTest

import history_store

SLIDERS = [27, 82, 18, 6.6, 24.0, 460.0]    # N, P, K, pH, T, R -> model recommends Groundnut


def _app():
    return AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py"), default_timeout=150)


def _run_dashboard(target="Jowar"):
    at = _app().run()
    for w, v in zip(at.slider, SLIDERS):
        w.set_value(v)
    at.selectbox[0].set_value(target)
    at.button[0].click()
    return at.run()


@pytest.fixture(scope="module")
def dash():
    return _run_dashboard("Jowar")


def _html(at):
    return " ".join(m.value for m in at.markdown)


def test_decision_returned_and_best_fit_show_recommended_not_target(dash):
    assert not dash.exception
    html = _html(dash)
    assert re.search(r'res-eyebrow">Decision returned · Groundnut<', html)
    assert re.search(r'Best fit for this soil</p>\s*<h2 class="res-crop">Groundnut</h2>', html)
    assert re.search(r"Analysed for \(your target crop\): <b>Jowar</b>", html)
    assert ("🌱 Recommended Crop", "Groundnut") in [(m.label, m.value) for m in dash.metric]


def test_fertilizer_card_defaults_to_recommended_crop_and_can_switch(dash):
    radio = [r for r in dash.radio if r.label == "Fertilizer advice for"][0]
    assert radio.value == "Recommended crop" and radio.options == ["Recommended crop", "Target crop"]
    assert "Fertilizer — Groundnut" in _html(dash)
    radio.set_value("Target crop")
    dash.run()
    assert "Fertilizer — Jowar" in _html(dash)


def test_dashboard_yield_caption_keeps_crops_separate(dash):
    cap = " ".join(c.value for c in dash.caption)
    assert "Target crop **Jowar**" in cap and "Recommended crop **Groundnut**" in cap


def test_history_page_shows_three_fields_and_not_recorded(tmp_path, monkeypatch):
    monkeypatch.setattr(history_store, "_PATH", str(tmp_path / "h.json"))
    history_store.add_run({"field": "A", "crop": "Jowar", "grown_crop": "Cotton", "recommended": "Groundnut",
                           "yield_kg_ha": 1369.0, "recommended_yield_kg_ha": 1500.0,
                           "nitrogen": 27, "phosphorus": 82, "potassium": 18, "ph": 6.6, "temperature": 24, "rainfall": 460})
    # legacy-style record: no grown crop, no recommended crop stored
    history_store.add_run({"field": "B", "crop": "Wheat", "yield_kg_ha": 3000.0,
                           "nitrogen": 50, "phosphorus": 40, "potassium": 30, "ph": 6.5, "temperature": 25, "rainfall": 700})
    at = _app().run()
    [r for r in at.radio if r.label == "Section"][0].set_value("History")
    at.run()
    assert not at.exception
    df = at.dataframe[0].value.set_index("Label")
    a, b = df.loc["A"], df.loc["B"]
    assert (a["Recommended"], a["Analysed for"], a["Grown"]) == ("Groundnut", "Jowar", "Cotton")
    assert (b["Recommended"], b["Analysed for"], b["Grown"]) == ("Unknown (older record)", "Wheat", "Not recorded")
    assert a["Yield — analysed crop (kg/ha)"] == 1369.0 and a["Yield — recommended crop (kg/ha)"] == 1500.0
