import sqlalchemy as sa
from flask import flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.main import main
from app.main.forms import VodSearchForm, VodSubmitForm
from app.models import MatchVod


@main.route("/index", methods=["GET", "POST"])
@main.route("/", methods=["GET", "POST"])
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


@main.route("/submit", methods=["GET", "POST"])
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


@main.route("/favorite/<int:vod_id>", methods=["POST"])
@login_required
def favorite(vod_id):
    vod = db.session.get(MatchVod, vod_id)

    if vod is None:
        return jsonify({"message": "MatchVod not found."}), 404

    if current_user.has_favorited(vod):
        return jsonify({"message:": "You have already favorited this MatchVod"}), 409

    current_user.favorite(vod)
    db.session.commit()
    return jsonify({"message": f"You have favorited MatchVod {vod.id}"}), 200


@main.route("/unfavorite/<int:vod_id>", methods=["POST"])
@login_required
def unfavorite(vod_id):
    vod = db.session.get(MatchVod, vod_id)

    if vod is None:
        return jsonify({"message": "MatchVod not found."}), 404

    if not current_user.has_favorited(vod):
        return (
            jsonify({"message:": "You already are not favoriting this MatchVod"}),
            409,
        )

    current_user.unfavorite(vod)
    db.session.commit()
    return jsonify({"message": f"You have unfavorited MatchVod {vod.id}"}), 200
