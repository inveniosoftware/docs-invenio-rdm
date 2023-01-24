#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
# This script is intended to automate the process for upgrading an
# Invenio-RDM v1.0 instance to v2.0.
# It should be placed in the instance directory of InvenioRDM v1.0 and
# executed there.

if [[ -f Pipfile && -f invenio.cfg ]]; then
	# check where we are DB-wise
	pipenv run invenio alembic stamp
	pipenv run invenio alembic upgrade

	# lock and install packages for InvenioRDM 2.0
	rm Pipfile.lock
	sed -e 's/1.0.0/2.0.0/' -i Pipfile
	invenio-cli packages lock
	invenio-cli install

	# find the migration script that comes with Invenio-App-RDM
	migration_script=$(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_1_0_records_to_2_0.py)

	# upgrade DB, migrate records
	pipenv run invenio alembic upgrade
	pipenv run invenio shell ${migration_script}
	pipenv run invenio index destroy --yes-i-know
	pipenv run invenio index init
	pipenv run invenio rdm-records rebuild-index

else

	echo "the current directory doesn't look like the home of an InvenioRDM 1.0 instance" >&2
	exit 1

fi
