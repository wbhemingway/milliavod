import secrets
from urllib.parse import urlencode

import requests
import sqlalchemy as sa
from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db, login
from app.forms import VodSearchForm, VodSubmitForm
from app.models import MatchVod, User


@login.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    form = VodSearchForm()
    results = []
    if form.validate_on_submit():
        p1name = form.p1name.data
        p2name = form.p2name.data
        p2character = form.p2character.data
        verifiedonly = form.verifiedonly.data
        base_query = sa.select(MatchVod)
        if verifiedonly:
            base_query = base_query.where(MatchVod.verified)
        if p1name != "":
            base_query = base_query.where(MatchVod.p1name.ilike(p1name))
        if p2name != "":
            base_query = base_query.where(MatchVod.p2name.ilike(p2name))
        if p2character != "Any":
            base_query = base_query.where(MatchVod.p2character == p2character)
        base_query = base_query.order_by(MatchVod.timesubmitted.desc())
        results = db.session.scalars(base_query).all()
    return render_template(
        "index.html", form=form, results=results, title="Search Matches"
    )


@app.route("/submit", methods=["GET", "POST"])
def submit_vod():
    form = VodSubmitForm()
    if form.validate_on_submit():
        vod = MatchVod(
            link=form.link.data,
            p1name=form.p1name.data,
            p2name=form.p2name.data,
            p2character=form.p2character.data,
            source=form.source.data if form.source.data != "" else None,
        )
        db.session.add(vod)
        db.session.commit()
        flash("Your match has been submitted")
        return redirect(url_for("index"))
    return render_template("submit.html", form=form, title="Submit Match")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    session["oauth2_state"] = secrets.token_urlsafe(16)

    querystring = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": session["oauth2_state"],
        }
    )

    return redirect(provider_data["authorize_url"] + "?" + querystring)


@app.route("/callback/<provider>")
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("index"))

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
                "oauth2_callback", provider=provider, _external=True
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
    return redirect(url_for("index"))
