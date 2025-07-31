import sqlalchemy as sa
from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.admin import admin
from app.decorators import admin_required
from app.models import MatchVod


@admin.route("/unverified_vods")
@login_required
@admin_required
def unverified_vods():
    query = (
        sa.select(MatchVod)
        .where(~MatchVod.verified)
        .order_by(MatchVod.timesubmitted.desc())
    )
    unvods = db.session.scalars(query).all()

    return render_template("admin/unverified_vods.html", unvods=unvods)


@admin.route("/verify_vod/<int:vod_id>", methods=["POST"])
@login_required
@admin_required
def verify_vod(vod_id):
    vod = db.session.get(MatchVod, vod_id)

    if vod is None:
        flash("There is not a vod with that ID")
        return redirect(url_for("admin.unverified_vods"))
    if vod.verified:
        flash("This VOD is already verified")
        return redirect(url_for("admin.unverified_vods"))

    vod.verify()
    db.session.commit()
    return redirect(url_for("admin.unverified_vods"))


@admin.route("/delete_vod/<int:vod_id>", methods=["POST"])
@login_required
@admin_required
def delete_vod(vod_id):
    vod = db.session.get(MatchVod, vod_id)

    if vod is None:
        flash("There is not a vod with that ID")
        return redirect(url_for("admin.unverified_vods"))

    vod.delete()
    db.session.commit()
    return redirect(url_for("admin.unverified_vods"))
