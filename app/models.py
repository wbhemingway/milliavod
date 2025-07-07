from datetime import datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from app import db


class MatchVod(db.Model):
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


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
