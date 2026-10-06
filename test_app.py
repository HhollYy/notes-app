import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db, Note


def setup_function():
    with app.app_context():
        db.drop_all()
        db.create_all()


def test_home_page_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_add_note():
    client = app.test_client()
    response = client.post(
        "/add",
        data={"title": "Test note", "content": "Hello", "color": "#EFCE7B"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test note" in response.data

    with app.app_context():
        assert Note.query.count() == 1