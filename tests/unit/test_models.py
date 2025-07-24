from app.models import MatchVod, User


def test_new_user():
    user = User(email="testemail@gmail.com", username="testemail")
    assert user.email == "testemail@gmail.com"
    assert user.username == "testemail"
    assert not user.is_admin
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(test_user):
    assert test_user.email == "testemail@gmail.com"
    assert test_user.username == "testemail"
    assert not test_user.is_admin
    assert test_user.is_authenticated
    assert test_user.is_active
    assert not test_user.is_anonymous


def test_new_match_vod():
    match_vod = MatchVod(
        link="youtube.com/testlink",
        p1name="test1",
        p2name="test2",
        source="testsource",
        p2character="Sol",
    )
    assert match_vod.link == "youtube.com/testlink"
    assert match_vod.p1name == "test1"
    assert match_vod.p2name == "test2"
    assert match_vod.source == "testsource"
    assert match_vod.p2character == "Sol"
    # not commited so will be none
    assert not match_vod.timesubmitted
    assert not match_vod.verified
    assert not match_vod.timeverified


def test_new_match_vod_with_fixture(test_match_vod):
    assert test_match_vod.link == "youtube.com/testlink"
    assert test_match_vod.p1name == "test1"
    assert test_match_vod.p2name == "test2"
    assert test_match_vod.source == "testsource"
    assert test_match_vod.p2character == "Sol"
    # not commited so will be none
    assert not test_match_vod.timesubmitted
    assert not test_match_vod.verified
    assert not test_match_vod.timeverified


def test_verify(test_match_vod):
    vod = test_match_vod
    vod.verify()

    assert vod.link == "youtube.com/testlink"
    assert vod.p1name == "test1"
    assert vod.p2name == "test2"
    assert vod.source == "testsource"
    assert vod.p2character == "Sol"
    # not commited so will be none
    assert not vod.timesubmitted
    assert vod.verified
    assert vod.timeverified is not None
