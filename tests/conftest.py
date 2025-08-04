import pytest

from app import create_app, db
from app.models import MatchVod, User
from config import TestConfig


@pytest.fixture(scope="session")
def app():

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def clean_db(app):
    with app.app_context():
        db.create_all()

        yield db

        db.drop_all()


@pytest.fixture(scope="function")
def test_user():
    user = User(email="testemail@gmail.com", username="testemail")
    return user


@pytest.fixture(scope="function")
def test_admin_user():
    admin_user = User(username="adminuser", email="admin@example.com", is_admin=True)
    return admin_user


@pytest.fixture(scope="function")
def test_match_vod():
    match_vod = MatchVod(
        link="youtube.com/testlink",
        p1name="test1",
        p2name="test2",
        source="testsource",
        p2character="Sol",
    )
    return match_vod


@pytest.fixture(scope="function")
def logged_in_client(test_client, clean_db):
    user = User(username="logged_in_user", email="logged@example.com")
    clean_db.session.add(user)
    clean_db.session.commit()

    with test_client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True
    yield test_client


@pytest.fixture(scope="function")
def logged_in_admin_client(test_client, clean_db):
    user = User(username="logged_in_user", email="logged@example.com", is_admin=True)
    clean_db.session.add(user)
    clean_db.session.commit()

    with test_client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True
    yield test_client


@pytest.fixture(scope="function")
def runner(app):
    return app.test_cli_runner()
