# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""OAI-PMH and Jobs Datastream migrator from InvenioRDM 13.0 to 14.0."""

import json

from click import secho
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_oaiserver.percolator import _build_percolator_index_name
from invenio_rdm_records.proxies import current_rdm_records
from invenio_search.proxies import current_search, current_search_client
from invenio_search.utils import build_alias_name
from opensearchpy.exceptions import RequestError


def update_oai_pmh_percolator():
    """Update oai pmh percolator mapping."""
    index = current_app.config["OAISERVER_RECORD_INDEX"]
    percolator_index = _build_percolator_index_name(index)
    record_index = build_alias_name(index)

    # Fetch the mapping from the "live" index (this will include custom fields)
    record_mapping = current_search_client.indices.get_mapping(index=record_index)
    assert len(record_mapping) == 1
    mappings = list(record_mapping.values())[0]["mappings"]
    mappings["properties"]["query"] = {"type": "percolator"}
    with open(current_search.mappings[index]) as fp:
        settings = json.load(fp)["settings"]
    percolator_body = {"settings": settings, "mappings": mappings}

    # Recreate the percolator index, to avoid mapping conflicts
    assert percolator_index != record_index
    current_search_client.indices.delete(index=percolator_index)
    current_search_client.indices.create(index=percolator_index, body=percolator_body)

    # Reindex all percolator queries from OAISets
    oaipmh_service = current_rdm_records.oaipmh_server_service
    oaipmh_service.rebuild_index(identity=system_identity)
    secho("updating oai-pmh percolator mapping was successfull.", fg="green")


def update_jobs_datastream_index():
    """Update jobs datastream index."""
    datastream = build_alias_name("job-logs")
    try:
        current_search_client.indices.rollover(alias=datastream)
    except RequestError:
        secho("No jobs have been used yet — no rollover needed.", fg="yellow")
    else:
        secho("Jobs datastream rollover was successfull.", fg="green")


def execute_upgrade():
    """Execute the upgrade from InvenioRDM 13.0 to 14.0.

    Please read the disclaimer on this module before thinking about executing
    this function!
    """
    update_oai_pmh_percolator()
    update_jobs_datastream_index()


# if the script is executed on its own, perform the upgrade
if __name__ == "__main__":
    execute_upgrade()
