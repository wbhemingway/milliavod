from app.models import User


def test_create_new_admin(runner, app, clean_db):
    email = "new_admin@example.com"
    username = "test_admin"

    result = runner.invoke(
        args=["db_inits", "create_admin", email, "--username", username]
    )

    assert f"Admin user {username}, {email} created" in result.output

    with app.app_context():
        admin_user = clean_db.session.scalar(
            clean_db.select(User).where(User.email == email)
        )
        assert admin_user is not None
        assert admin_user.username == username
        assert admin_user.email == email
        assert admin_user.is_admin is True


def test_create_new_admin_without_username(runner, app, clean_db):
    email = "new_admin@example.com"

    result = runner.invoke(args=["db_inits", "create_admin", email])

    assert f"Admin user {email.split('@')[0]}, {email} created" in result.output

    with app.app_context():
        admin_user = clean_db.session.scalar(
            clean_db.select(User).where(User.email == email)
        )
        assert admin_user is not None
        assert admin_user.username == email.split("@")[0]
        assert admin_user.email == email
        assert admin_user.is_admin is True


def test_make_user_admin(runner, app, clean_db):
    email = "new_admin@example.com"
    username = "test_admin"
    user = User(username=username, email=email)
    clean_db.session.add(user)
    clean_db.session.commit()

    result = runner.invoke(args=["db_inits", "create_admin", email])

    assert f"User {email} already exists, is now admin." in result.output

    with app.app_context():
        admin_user = clean_db.session.scalar(
            clean_db.select(User).where(User.email == email)
        )
        assert admin_user is not None
        assert admin_user.username == "test_admin"
        assert admin_user.email == email
        assert admin_user.is_admin is True


def test_create_admin_already_admin(runner, app, clean_db):
    email = "new_admin@example.com"

    result = runner.invoke(args=["db_inits", "create_admin", email])

    result = runner.invoke(args=["db_inits", "create_admin", email])

    assert f"User {email} is already an admin." in result.output

    with app.app_context():
        admin_user = clean_db.session.scalar(
            clean_db.select(User).where(User.email == email)
        )
        assert admin_user is not None
        assert admin_user.username == email.split("@")[0]
        assert admin_user.email == email
        assert admin_user.is_admin is True

