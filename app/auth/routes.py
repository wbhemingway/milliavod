import secrets
from urllib.parse import urlencode

import requests
from flask import abort, current_app, flash, redirect, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.auth import auth
from app.models import User


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    session["oauth2_state"] = secrets.token_urlsafe(16)

    querystring = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "auth.oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": session["oauth2_state"],
        }
    )

    return redirect(provider_data["authorize_url"] + "?" + querystring)


@auth.route("/callback/<provider>")
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("main.index"))

    if "code" not in request.args:
        abort(401)

    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "auth.oauth2_callback", provider=provider, _external=True
            ),
        },
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        print(response.status_code)
        print("not 200")
        abort(401)
    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        print("not oauth2_token")
        abort(401)

    response = requests.get(
        provider_data["userinfo"]["url"],
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
    )
    if response.status_code != 200:
        print("not 200 2")
        abort(401)
    email = provider_data["userinfo"]["email"](response.json())

    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        user = User(email=email, username=email.split("@")[0])
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    return redirect(url_for("main.index"))
