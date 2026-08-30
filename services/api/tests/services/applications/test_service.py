from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models.application import Application
from app.services.applications.service import (
    create_application,
    delete_application,
    get_application,
    update_application,
)


def application_data(application_id: str) -> dict:
    return {
        "application_id": application_id,
        "node_id": "test-node",
        "package_id": "test.package",
        "name": "Test Application",
        "version": "1.0.0",
        "install_state": "installed",
        "launch_info": {},
        "capabilities": [],
        "store_metadata": {},
    }


def test_create_application():
    db = SessionLocal()

    try:
        application = create_application(
            db,
            application_data("service-application"),
        )

        assert application.application_id == "service-application"
        assert application.node_id == "test-node"
        assert application.package_id == "test.package"
        assert application.name == "Test Application"
        assert application.version == "1.0.0"
        assert application.install_state == "installed"
        assert application.launch_info == {}
        assert application.capabilities == []
        assert application.store_metadata == {}
    finally:
        application = db.get(Application, "service-application")
        if application is not None:
            db.delete(application)
            db.commit()
        db.close()


def test_get_application():
    db = SessionLocal()

    try:
        application = Application(
            **application_data("get-application"),
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        result = get_application(
            db,
            "get-application",
        )

        assert result is not None
        assert result.application_id == "get-application"
        assert result.name == "Test Application"
    finally:
        application = db.get(Application, "get-application")
        if application is not None:
            db.delete(application)
            db.commit()
        db.close()


def test_update_application():
    db = SessionLocal()

    try:
        application = Application(
            **application_data("update-application"),
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        result = update_application(
            db,
            application,
            {
                "name": "New Name",
                "version": "2.0.0",
            },
        )

        assert result.name == "New Name"
        assert result.version == "2.0.0"
    finally:
        application = db.get(Application, "update-application")
        if application is not None:
            db.delete(application)
            db.commit()
        db.close()


def test_delete_application():
    db = SessionLocal()

    try:
        application = Application(
            **application_data("delete-application"),
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        delete_application(
            db,
            application,
        )

        assert db.get(
            Application,
            "delete-application",
        ) is None
    finally:
        db.close()


def test_create_application_rejects_duplicate():
    db = SessionLocal()

    try:
        application = Application(
            **application_data("duplicate-application"),
        )

        db.add(application)
        db.commit()

        try:
            create_application(
                db,
                application_data("duplicate-application"),
            )

            assert False, "Expected duplicate application error"
        except (ValueError, IntegrityError):
            db.rollback()
    finally:
        application = db.get(Application, "duplicate-application")
        if application is not None:
            db.delete(application)
            db.commit()
        db.close()
