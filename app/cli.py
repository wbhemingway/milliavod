import csv
import json

import click
from flask import Blueprint
from flask.cli import with_appcontext

from app import db
from app.models import MatchVod, User

bp = Blueprint("cli", __name__, cli_group="db_inits")


@bp.cli.command("create_admin")
@click.argument("email")
@click.option("--username", help="Username for the admin user(optional).")
@with_appcontext
def create_admin(email, username):
    """Creates an admin user or promotes an existing user to admin using a given email."""
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user:
        if user.is_admin:
            click.echo(f"User {email} is already an admin.")
        else:
            user.is_admin = True
            db.session.commit()
            click.echo(f"User {email} already exists, is now admin.")
    else:
        new_admin = User(
            username=username or email.split("@")[0], email=email, is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        click.echo(f"Admin user {new_admin.username}, {new_admin.email} created")


@bp.cli.command("import_matches")
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--file_type",
    type=click.Choice(["csv", "json"], case_sensitive=False),
    default="json",
    help="Type of the input file (csv or json).",
)
@with_appcontext
def import_matches(file_path, file_type):
    """Imports real match VODs (and their timestamps) from a specified local CSV or JSON file."""
    click.echo(f"Attempting to import matches from {file_path} (Type: {file_type})...")
    imported_vod_count = 0
    imported_timestamp_count = 0
    skipped_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            if file_type == "csv":
                click.echo("csv files are not yet supported")
                return
                reader = csv.DictReader(f)
                match_data = list(reader)
            elif file_type == "json":
                match_data = json.load(f)
            else:
                click.echo(f"Error: Unsupported file type '{file_type}'.")
                return

        if not match_data:
            click.echo("No data found in the file.")
            return

        for row in match_data:
            try:
                link = row.get("link")
                p1name = row.get("p1name")
                p2character = row.get("p2character")
                p2name = row.get("p2name")
                source = row.get("source", None)
                verified = row.get("verified", "false") == "true"

                if not all([link, p1name, p2character, p2name]):
                    click.echo(f"Skipping row due to missing required VOD data: {row}")
                    skipped_count += 1
                    continue

                existing_vod = db.session.scalar(
                    db.select(MatchVod).where(MatchVod.link == link)
                )
                if existing_vod:
                    click.echo(f"Skipping VOD with link '{link}' as it already exists.")
                    skipped_count += 1
                    continue
                vod = MatchVod(
                    link=link,
                    p1name=p1name,
                    p2character=p2character,
                    p2name=p2name,
                    source=source if source else None,
                    verified=verified,
                )
                db.session.add(vod)
                db.session.commit()
                imported_vod_count += 1

            except Exception as row_e:
                click.echo(f"Error processing row {row}: {row_e}")
                skipped_count += 1
                db.session.rollback()

        db.session.commit()
        click.echo(
            f"Successfully imported {imported_vod_count} matches and {imported_timestamp_count} timestamps."
        )
        if skipped_count > 0:
            click.echo(f"Skipped {skipped_count} rows due to errors or existing VODs.")

    except FileNotFoundError:
        click.echo(f"Error: File not found at {file_path}")
    except Exception as e:
        db.session.rollback()
        click.echo(f"An unexpected error occurred: {e}")
