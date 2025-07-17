from datetime import datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from app import db, login

favorites = sa.Table(
    "favorites",
    db.metadata,
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "matchvod_id",
        sa.Integer,
        sa.ForeignKey("matchvod.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class MatchVod(db.Model):
    __tablename__ = "matchvod"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    link: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    p1name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    p2character: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    p2name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    timesubmitted: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    verified: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    timeverified: so.Mapped[datetime] = so.mapped_column(nullable=True)
    source: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    favoriting_users: so.WriteOnlyMapped["User"] = so.relationship(
        secondary=favorites, back_populates="favorited_vods", passive_deletes=True
    )

    def verify(self):
        if not self.verified:
            self.verified = True
            self.timeverified = datetime.now(timezone.utc)

    def delete(self):
        db.session.delete(self)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    favorited_vods: so.WriteOnlyMapped["MatchVod"] = so.relationship(
        secondary=favorites, back_populates="favoriting_users", passive_deletes=True
    )
    is_admin: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, default=False, nullable=True
    )

    def favorite(self, vod):
        if not self.has_favorited(vod):
            self.favorited_vods.add(vod)

    def unfavorite(self, vod):
        if self.has_favorited(vod):
            self.favorited_vods.remove(vod)

    def has_favorited(self, vod):
        query = self.favorited_vods.select().where(MatchVod.id == vod.id)
        return db.session.scalar(query) is not None


@login.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
