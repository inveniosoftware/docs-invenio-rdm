# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Ensure alembic table exists."""

from alembic.migration import MigrationContext
from click import secho
from flask import current_app
from invenio_db.utils import create_alembic_version_table
from sqlalchemy import inspect, text


def main():
    """Check if alembic_version table exists and if not fill it like alembic stamp."""

    alembic = current_app.extensions["invenio-db"].alembic
    db = current_app.extensions["sqlalchemy"]

    if inspect(db.engine).has_table("alembic_version"):
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT EXISTS (SELECT 1 FROM alembic_version)"))
            if result.scalar():
                msg = "Everything is fine, the alembic_version table exists and has values in it"

            else:
                with db.engine.begin() as connection:
                    context = MigrationContext.configure(connection)
                    all_heads = alembic.script_directory.revision_map._real_heads
                    context.stamp(alembic.script_directory, tuple(all_heads))
                msg = "Table has been filled"

    else:
        create_alembic_version_table()
        msg = "Table has been created and filled"

    secho(msg, fg="green")


if __name__ == "__main__":
    main()
