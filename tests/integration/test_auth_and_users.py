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
