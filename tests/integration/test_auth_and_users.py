from app.models import User


def test_google_login_redirect(test_client):
    response = test_client.get("/auth/authorize/google")
    assert response.status_code == 302
    assert "accounts.google.com/o/oauth2/auth" in response.headers["Location"]


def test_logout_unauthenticated_redirect(test_client):
    response = test_client.get("auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Search Millia Matches" in response.data
    assert b"Login" in response.data
    assert b"Logout" not in response.data


def test_logout_authenticated(logged_in_client):
    response = logged_in_client.get("auth/logout", follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b"You have been logged" in response.data
    assert b"Favorited Only" not in response.data


def test_admin_page_redirects_unauthenticated(test_client):
    response = test_client.get("admin/unverified_vods", follow_redirects=True)
    assert response.status_code == 200
    assert b"Favorited Only" not in response.data


def test_admin_page_redirects_unauthorized(logged_in_client):
    response = logged_in_client.get("admin/unverified_vods", follow_redirects=True)
    assert response.status_code == 403
    assert b"Forbidden" in response.data
    assert b"Back" in response.data


def test_admin_page_authorized(logged_in_admin_client):
    response = logged_in_admin_client.get(
        "admin/unverified_vods", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Unverified Vods" in response.data


def test_user_creation(app, clean_db, test_user):
    with app.app_context():
        clean_db.session.add(test_user)
        clean_db.session.commit()

        user = clean_db.session.scalar(
            clean_db.select(User).where(User.email == test_user.email)
        )

        assert user.email == test_user.email
        assert user.username == test_user.username
        assert user.id is not None
