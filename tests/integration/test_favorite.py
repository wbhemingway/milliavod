from app.models import MatchVod, User


def test_favorite_vod(logged_in_client, clean_db, test_match_vod):
    clean_db.session.add(test_match_vod)
    clean_db.session.commit()

    vod = MatchVod.query.first()
    favorited_vods = clean_db.session.scalars(
        clean_db.select(MatchVod).where(MatchVod.favoriting_users.any(User.id == 1))
    ).all()
    assert vod is not None
    assert favorited_vods == []

    response = logged_in_client.post("/favorite/1", follow_redirects=True)
    assert response.status_code == 200

    vod = MatchVod.query.first()
    favorited_vods = clean_db.session.scalars(
        clean_db.select(MatchVod).where(MatchVod.favoriting_users.any(User.id == 1))
    ).all()
    assert favorited_vods[0].id == vod.id


def test_favorite_nonexistent(logged_in_client, clean_db):
    response = logged_in_client.post("/favorite/1")
    assert response.status_code == 404
    assert b"MatchVod not found" in response.data


def test_unfavorite_nonexistent(logged_in_client, clean_db):
    response = logged_in_client.post("/unfavorite/1")
    assert response.status_code == 404
    assert b"MatchVod not found" in response.data


def test_unfavorite_notfavorited(logged_in_client, clean_db, test_match_vod):
    clean_db.session.add(test_match_vod)
    clean_db.session.commit()

    response = logged_in_client.post("/unfavorite/1")
    assert response.status_code == 409
    assert b"You already are not favoriting this MatchVod" in response.data


def test_favorite_favorited(logged_in_client, clean_db, test_match_vod):
    clean_db.session.add(test_match_vod)
    clean_db.session.commit()

    response = logged_in_client.post("/favorite/1")
    response = logged_in_client.post("/favorite/1")

    assert b"You have already favorited this MatchVod" in response.data
    assert response.status_code == 409


def test_unfavorite_vod(logged_in_client, clean_db, test_match_vod):
    clean_db.session.add(test_match_vod)
    clean_db.session.commit()

    vod = MatchVod.query.first()
    favorited_vods = clean_db.session.scalars(
        clean_db.select(MatchVod).where(MatchVod.favoriting_users.any(User.id == 1))
    ).all()
    assert vod is not None
    assert favorited_vods == []

    response = logged_in_client.post("/favorite/1", follow_redirects=True)
    assert response.status_code == 200

    vod = MatchVod.query.first()
    favorited_vods = clean_db.session.scalars(
        clean_db.select(MatchVod).where(MatchVod.favoriting_users.any(User.id == 1))
    ).all()
    assert favorited_vods[0].id == vod.id

    response = logged_in_client.post("/unfavorite/1", follow_redirects=True)

    assert response.status_code == 200

    vod = MatchVod.query.first()
    favorited_vods = clean_db.session.scalars(
        clean_db.select(MatchVod).where(MatchVod.favoriting_users.any(User.id == 1))
    ).all()
    assert favorited_vods == []
