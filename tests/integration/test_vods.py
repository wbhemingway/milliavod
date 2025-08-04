from app.models import MatchVod


def test_submit_vod(test_client, clean_db):
    form_data = {
        "link": "www.youtube.com/testlink",
        "p1name": "MilliaTest",
        "p2name": "OpponentTest",
        "p2character": "Sol",
        "source": "testsource",
    }
    response = test_client.post("/submit", data=form_data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Your match has been submitted" in response.data

    vod = clean_db.session.scalar(
        clean_db.select(MatchVod).where(MatchVod.link == "www.youtube.com/testlink")
    )

    assert vod.id is not None
    assert vod.link == "www.youtube.com/testlink"
    assert vod.p1name == "MilliaTest"
    assert vod.p2name == "OpponentTest"
    assert vod.p2character == "Sol"
    assert vod.source == "testsource"


def test_unverified_favorite_vod(test_client):
    response = test_client.post("/favorite/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"Please log in to access this" in response.data


def test_unverified_unfavorite_vod(test_client):
    response = test_client.post("/unfavorite/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"Please log in to access this" in response.data


def test_search_vod_any(clean_db, test_match_vod, test_client, app):
    with app.app_context():
        clean_db.session.add(test_match_vod)
        clean_db.session.commit()

    form_data = {
        "p1name": "",
        "p2name": "",
        "p2character": "Any",
    }
    response = test_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"test1" in response.data
    assert b"test2" in response.data


def test_search_vods_by_p1name(test_client, app, clean_db):
    with app.app_context():
        vod1 = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
            verified=True,
        )
        vod2 = MatchVod(
            link="http://v2.com",
            p1name="AnotherMillia",
            p2character="Sol",
            p2name="SolPlayer",
            verified=True,
        )
        clean_db.session.add_all([vod1, vod2])
        clean_db.session.commit()

    form_data = {
        "p1name": "MilliaPlayer",
        "p2name": "",
        "p2character": "Any",
        "favoritedonly": False,
        "verifiedonly": True,
    }
    response = test_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"MilliaPlayer" in response.data
    assert b"KyPlayer" in response.data
    assert b"AnotherMillia" not in response.data


def test_search_vods_by_p2name(test_client, app, clean_db):
    with app.app_context():
        vod1 = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
            verified=True,
        )
        vod2 = MatchVod(
            link="http://v2.com",
            p1name="AnotherMillia",
            p2character="Sol",
            p2name="SolPlayer",
            verified=True,
        )
        clean_db.session.add_all([vod1, vod2])
        clean_db.session.commit()

    form_data = {
        "p1name": "",
        "p2name": "KyPlayer",
        "p2character": "Any",
        "verifiedonly": True,
    }
    response = test_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"MilliaPlayer" in response.data
    assert b"KyPlayer" in response.data
    assert b"AnotherMillia" not in response.data


def test_search_vods_by_p2character(test_client, app, clean_db):
    with app.app_context():
        vod1 = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
            verified=True,
        )
        vod2 = MatchVod(
            link="http://v2.com",
            p1name="AnotherMillia",
            p2character="Sol",
            p2name="SolPlayer",
            verified=True,
        )
        clean_db.session.add_all([vod1, vod2])
        clean_db.session.commit()

    form_data = {
        "p1name": "MilliaPlayer",
        "p2name": "",
        "p2character": "Ky",
        "verifiedonly": True,
    }
    response = test_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"MilliaPlayer" in response.data
    assert b"KyPlayer" in response.data
    assert b"AnotherMillia" not in response.data


def test_admin_verify(logged_in_admin_client, app, clean_db):
    with app.app_context():
        vod = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
        )
        clean_db.session.add(vod)
        clean_db.session.commit()

    response = logged_in_admin_client.post("/admin/verify_vod/1")

    form_data = {
        "p1name": "",
        "p2name": "",
        "p2character": "Any",
        "verifiedonly": True,
    }
    response = logged_in_admin_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"MilliaPlayer" in response.data
    assert b"KyPlayer" in response.data
    assert b"AnotherMillia" not in response.data


def test_admin_verify_nonexistent(logged_in_admin_client):
    response = logged_in_admin_client.post("/admin/verify_vod/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"There is not a vod with that ID" in response.data


def test_admin_verify_verified(logged_in_admin_client, app, clean_db):
    with app.app_context():
        vod = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
        )
        clean_db.session.add(vod)
        clean_db.session.commit()

    response = logged_in_admin_client.post("/admin/verify_vod/1")

    response = logged_in_admin_client.post("/admin/verify_vod/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"This VOD is already verified" in response.data


def test_admin_delete(logged_in_admin_client, app, clean_db):
    with app.app_context():
        vod = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
        )
        clean_db.session.add(vod)
        clean_db.session.commit()

    response = logged_in_admin_client.post("/admin/delete_vod/1")

    form_data = {
        "p1name": "",
        "p2name": "",
        "p2character": "Any",
    }
    response = logged_in_admin_client.post("/", data=form_data)

    assert response.status_code == 200
    assert b"KyPlayer" not in response.data


def test_admin_delete_nonexistent(logged_in_admin_client):

    response = logged_in_admin_client.post("/admin/delete_vod/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"There is not a vod with that ID" in response.data


def test_search_favorite(logged_in_client, app, clean_db):
    with app.app_context():
        vod = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
        )
        clean_db.session.add(vod)
        clean_db.session.commit()

    response = logged_in_client.post("/favorite/1")

    form_data = {
        "p1name": "",
        "p2name": "",
        "p2character": "Any",
        "favoritedonly": True,
    }
    response = logged_in_client.post("/", data=form_data)

    assert response.status_code == 200
    assert b"KyPlayer" in response.data


def test_search_favorite_and_verified(logged_in_client, app, clean_db):
    with app.app_context():
        vod = MatchVod(
            link="http://v1.com",
            p1name="MilliaPlayer",
            p2character="Ky",
            p2name="KyPlayer",
            verified=True,
        )
        clean_db.session.add(vod)
        clean_db.session.commit()

    response = logged_in_client.post("/favorite/1")

    form_data = {
        "p1name": "",
        "p2name": "",
        "p2character": "Any",
        "favoritedonly": True,
        "verifiedonly": True,
    }
    response = logged_in_client.post("/", data=form_data)

    assert response.status_code == 200
    assert b"KyPlayer" in response.data
