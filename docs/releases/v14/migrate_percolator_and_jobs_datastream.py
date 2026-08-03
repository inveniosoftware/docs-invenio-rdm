# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""OAI-PMH and Jobs Datastream migrator from InvenioRDM 13.0 to 14.0."""

from click import secho
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_oaiserver.percolator import _build_percolator_index_name
from invenio_rdm_records.proxies import current_rdm_records
from invenio_search.proxies import current_search_client
from invenio_search.utils import build_alias_name


def update_oai_pmh_percolator():
    """Update oai pmh percolator mapping."""
    index = current_app.config["OAISERVER_RECORD_INDEX"]
    percolator_index = _build_percolator_index_name(index)
    record_index = build_alias_name(index)

    # Fetch the mapping from the "live" index (this will include custom fields)
    record_mapping = current_search_client.indices.get_mapping(index=record_index)
    assert len(record_mapping) == 1
    percolator_mappings = list(record_mapping.values())[0]["mappings"]

    # Update the mapping
    current_search_client.indices.put_mapping(
        index=percolator_index,
        body=percolator_mappings,
    )

    # Reindex all percolator queries from OAISets
    oaipmh_service = current_rdm_records.oaipmh_server_service
    oaipmh_service.rebuild_index(identity=system_identity)
    secho("updating oai-pmh percolator mapping was successfull.", fg="green")


def update_jobs_datastream_index():
    """Update jobs datastream index."""
    datastream = build_alias_name("job-logs")
    current_search_client.indices.rollover(alias=datastream)
    secho("jobs datastream rollover was successfull.", fg="green")


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
