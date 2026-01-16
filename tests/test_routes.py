from app import app

def test_home_route():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200

def test_create_contest_page():
    client = app.test_client()
    r = client.get("/create")
    assert r.status_code in (200, 302)
