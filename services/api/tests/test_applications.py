from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.application import Application

client = TestClient(app)


def test_create_application():
    payload = {
        "application_id": "test-application",
        "node_id": "test-node",
        "package_id": "com.test.app",
        "name": "test application",
        "version": "1.0.0",
        "install_state": "installed",
        "launch_info": {},
        "capabilities": [],
        "store_metadata": {},
    }

    response = client.post("/api/v1/applications", json=payload)

    assert response.status_code == 201
    assert response.json()["application_id"] == "test-application"

    db = SessionLocal()
    try:
        application = db.get(Application, "test-application")
        if application is not None:
            db.delete(application)
            db.commit()
    finally:
        db.close()


def test_get_application():
    db = SessionLocal()

    application = Application(
        application_id="get-application",
        node_id="node",
        package_id="package",
        name="get application",
        version="1.0",
        install_state="installed",
        launch_info={},
        capabilities=[],
        store_metadata={},
    )

    db.add(application)
    db.commit()

    db.close()

    try:
        response = client.get("/api/v1/applications/get-application")

        assert response.status_code == 200
        assert response.json()["application_id"] == "get-application"
        assert response.json()["name"] == "get application"

    finally:
        db = SessionLocal()
        try:
            application = db.get(Application, "get-application")
            if application is not None:
                db.delete(application)
                db.commit()
        finally:
            db.close()
