import sqlalchemy as sa
from flask import flash, redirect, render_template, url_for

from app import app, db
from app.forms import VodSearchForm, VodSubmitForm
from app.models import MatchVod


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
