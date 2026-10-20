"""End-to-end API tests: analysis -> DB -> History -> chatbot, persistence and isolation."""
import sqlite3
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.database import engine, init_db
from backend.config import DATABASE_URL

SOIL = dict(nitrogen=27, phosphorus=82, potassium=18, ph=6.6, temperature=24, rainfall=460)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:      # runs lifespan -> init_db()
        yield c


def _login(client, name):
    r = client.post("/api/auth/register", json={"username": name, "password": "secret123"})
    assert r.status_code in (200, 201), r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _relogin(client, name):
    r = client.post("/api/auth/login", json={"username": name, "password": "secret123"})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_three_crop_fields_stored_independently(client):
    h = _login(client, "farmer_a")
    # recommended=Groundnut (model), analysed=Jowar (user), grown=Cotton (farmer)
    r = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar", "grown_crop": "Cotton", "label": "North"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert (body["recommended_crop"], body["chosen_crop"], body["grown_crop"]) == ("Groundnut", "Jowar", "Cotton")
    row = client.get("/api/history", headers=h).json()["items"][0]
    assert (row["recommended_crop"], row["chosen_crop"], row["grown_crop"]) == ("Groundnut", "Jowar", "Cotton")


def test_grown_crop_not_auto_filled_when_not_recorded(client):
    h = _login(client, "farmer_b")
    client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar"})
    row = client.get("/api/history", headers=h).json()["items"][0]
    assert row["grown_crop"] is None                      # UI renders this as "Not recorded"
    assert row["recommended_crop"] == "Groundnut" and row["chosen_crop"] == "Jowar"
    # recording it later is explicit and leaves the other two fields alone
    r = client.patch(f"/api/history/{row['id']}", headers=h, json={"grown_crop": "Wheat"})
    assert r.json()["grown_crop"] == "Wheat"
    assert r.json()["recommended_crop"] == "Groundnut" and r.json()["chosen_crop"] == "Jowar"


def test_dashboard_and_history_yields_agree(client):
    h = _login(client, "farmer_c")
    live = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar", "save": False}).json()
    saved = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar"}).json()
    item = client.get(f"/api/history/{saved['id']}", headers=h).json()
    assert item["predicted_yield_kg_ha"] == live["predicted_yield_kg_ha"] == live["yields_by_crop"]["Jowar"]
    assert item["recommended_yield_kg_ha"] == live["yields_by_crop"]["Groundnut"]
    assert item["yields_by_crop"] == live["yields_by_crop"]
    assert item["fertilizer"]["recommended_crop_fertilizer"]["crop"] == "Groundnut"


def test_persistence_after_logout_login_and_new_session(client):
    h = _login(client, "farmer_d")
    pid = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar", "grown_crop": "Cotton"}).json()["id"]
    engine.dispose()                                  # drop pooled connections ("restart")
    init_db()
    h2 = _relogin(client, "farmer_d")                 # brand-new token = logout + login
    item = client.get(f"/api/history/{pid}", headers=h2).json()
    assert item["grown_crop"] == "Cotton" and item["recommended_crop"] == "Groundnut"


def test_expired_or_bad_token_is_401_and_does_not_delete_rows(client):
    h = _login(client, "farmer_e")
    pid = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar"}).json()["id"]
    bad = {"Authorization": "Bearer not.a.valid.token"}
    assert client.get("/api/history", headers=bad).status_code == 401
    assert client.get(f"/api/history/{pid}", headers=_relogin(client, "farmer_e")).status_code == 200


def test_account_isolation_history_and_chat(client):
    ha, hb = _login(client, "iso_a"), _login(client, "iso_b")
    pa = client.post("/api/predict", headers=ha, json={**SOIL, "crop": "Jowar", "grown_crop": "Cotton"}).json()["id"]
    assert client.get("/api/history", headers=hb).json()["total"] == 0
    assert client.get(f"/api/history/{pa}", headers=hb).status_code == 404
    assert client.patch(f"/api/history/{pa}", headers=hb, json={"grown_crop": "Wheat"}).status_code == 404
    assert client.delete(f"/api/history/{pa}", headers=hb).status_code == 404
    assert client.post("/api/chat", headers=hb, json={"message": "yield?", "prediction_id": pa}).status_code == 404
    # B's chat has no context from A's analysis
    r = client.post("/api/chat", headers=hb, json={"message": "ऊसाचे उत्पादन किती?"}).json()
    assert r["prediction_id"] is None


def test_chat_marathi_sugarcane_via_api_uses_this_users_analysis(client):
    h = _login(client, "chat_user")
    saved = client.post("/api/predict", headers=h, json={**SOIL, "crop": "Jowar"}).json()
    r = client.post("/api/chat", headers=h, json={"message": "उस्म्याच्या पिकाचे अपेक्षित उत्पादन किती आहे?"}).json()
    assert r["lang"] == "mr" and r["prediction_id"] == saved["id"]
    assert f"{saved['yields_by_crop']['Sugarcane']:,.1f}" in r["answer"]
    assert f"{saved['yields_by_crop']['Wheat']:,.1f}" not in r["answer"]
    assert "kg/ha" in r["answer"]


def test_old_record_without_new_fields_is_read_safely_not_relabelled(client):
    """Simulate a row saved before grown_crop / recommended_yield / fertilizer extras existed."""
    h = _login(client, "legacy_user")
    uid = client.get("/api/auth/me", headers=h).json()["id"]
    path = DATABASE_URL.replace("sqlite:///", "")
    con = sqlite3.connect(path)
    con.execute(
        "INSERT INTO predictions (user_id, created_at, nitrogen, phosphorus, potassium, ph, temperature, rainfall,"
        " chosen_crop, recommended_crop, predicted_yield_kg_ha, top_crops, soil_analysis, fertilizer, yield_prediction)"
        " VALUES (?, '2025-01-01 00:00:00', 50, 40, 30, 6.5, 25, 700, 'Wheat', 'Cotton', 3000.0, '[]', '{}', '{}', '{}')",
        (uid,),
    )
    con.commit(); con.close()
    item = client.get("/api/history", headers=h).json()["items"][0]
    assert item["chosen_crop"] == "Wheat" and item["recommended_crop"] == "Cotton"   # exactly as stored
    assert item["grown_crop"] is None and item["recommended_yield_kg_ha"] is None    # not guessed
    full = client.get(f"/api/history/{item['id']}", headers=h)
    assert full.status_code == 200 and full.json()["yields_by_crop"] == {}
    # chatbot on an old record: sugarcane yield is calculated now (labelled) from stored soil, never borrowed
    ans = client.post("/api/chat", headers=h, json={"message": "sugarcane yield?", "prediction_id": item["id"], "lang": "en"}).json()["answer"]
    assert "calculated it now" in ans and "3,000.0" not in ans
