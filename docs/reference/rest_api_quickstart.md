# Quickstart

This guide will walk you through the full sequence of requests to create and publish a record in InvenioRDM, including file uploads. We'll use cURL commands for each step.

## Prerequisites

- Access to an InvenioRDM instance (we'll use the InvenioRDM demo instance at <https://inveniordm.web.cern.ch> for this example)
- An API token for authentication
- `curl` installed on your machine

### Create a Draft upload

First, create a draft upload with a minimal set of metadata.

```bash
curl -i -X POST https://inveniordm.web.cern.ch/api/records \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${TOKEN}" \
     -d '
{
  "metadata": {
    "title": "Poltergeist activity readings dataset",
    "creators": [
      {
        "person_or_org": {
          "given_name": "Josiah",
          "family_name": "Carberry",
          "type": "personal",
          "identifiers": [{"identifier": "0000-0002-1825-0097"}]
        },
        "affiliations": [{"name": "Brown University"}]
      }
    ],
    "publisher": "InvenioRDM",
    "publication_date": "2024-05-14",
    "resource_type": {"id": "dataset"}
  }
}'
```

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": "ha4g3-7x208",
  "is_draft": true,
  "is_published": false,
  "status": "draft",
  "created": "2024-05-14T12:02:42.925027+00:00",
  "updated": "2024-05-14T12:02:43.001866+00:00",
  "expires_at": "2024-05-14 12:02:42.925074",
  "revision_id": 4,
  "metadata": {
    "creators": [
      {
        "affiliations": [{ "name": "Brown University" }],
        "person_or_org": {
          "family_name": "Carberry",
          "given_name": "Josiah",
          "type": "personal",
          "identifiers": [
            { "identifier": "0000-0002-1825-0097", "scheme": "orcid" }
          ],
          "name": "Carberry, Josiah"
        }
      }
    ],
    "resource_type": {
      "id": "dataset",
      "title": { "de": "Datensatz", "en": "Dataset" }
    },
    "publication_date": "2024-05-14",
    "title": "Poltergeist activity readings dataset",
    "publisher": "InvenioRDM"
  },
  "access": {
    "files": "public",
    "record": "public",
    "status": "metadata-only",
    "embargo": { "reason": null, "active": false }
  },
  "parent": {
    "access": { "links": [], "owned_by": [{ "user": 25 }] },
    "id": "bhgqt-2ke02",
    "communities": {}
  },
  "versions": { "is_latest_draft": true, "index": 1, "is_latest": false },
  "files": { "enabled": true, "order": [] },
  "pids": {},
  "links": {
    "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft",
    "self_html": "https://inveniordm.web.cern.ch/uploads/ha4g3-7x208",
    "self_iiif_manifest": "https://inveniordm.web.cern.ch/api/iiif/draft:ha4g3-7x208/manifest",
    "self_iiif_sequence": "https://inveniordm.web.cern.ch/api/iiif/draft:ha4g3-7x208/sequence/default",
    "files": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files",
    "archive": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files-archive",
    "record": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208",
    "record_html": "https://inveniordm.web.cern.ch/records/ha4g3-7x208",
    "publish": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/actions/publish",
    "review": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/review",
    "versions": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/versions",
    "access_links": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/access/links",
    "reserve_doi": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/pids/doi",
    "communities": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/communities",
    "communities-suggestions": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/communities-suggestions",
    "requests": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/requests"
  }
}
```

### Upload a file

Initialize the file upload for a `data.csv` file.

```bash
curl -i -X POST https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${TOKEN}" \
     -d '
[
  {"key": "data.csv"}
]'
```

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "enabled": true,
  "default_preview": null,
  "order": [],
  "entries": [
    {
      "key": "data.csv",
      "status": "pending",
      "created": "2024-05-14T12:14:33.825316+00:00",
      "updated": "2024-05-14T12:14:33.830465+00:00",
      "metadata": null,
      "links": {
        "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv",
        "content": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/content",
        "commit": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/commit"
      }
    }
  ],
  "links": {
    "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files",
    "archive": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files-archive"
  }
}
```

Upload the file content.

!!! note
    Replace `path/to/your/local/file/myfile.txt` with the actual path to the file you want to upload.

```bash
curl -i -X PUT https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/content \
     -H "Content-Type: application/octet-stream" \
     -H "Authorization: Bearer ${TOKEN}" \
     --data-binary @path/to/your/local/file/data.csv
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "data.csv",
  "created": "2024-05-14T12:14:33.825316+00:00",
  "updated": "2024-05-14T12:14:33.830465+00:00",
  "status": "pending",
  "metadata": null,
  "links": {
    "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv",
    "content": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/content",
    "commit": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/commit"
  }
}
```

Commit the uploaded file.

```bash
curl -i -X POST https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/commit \
     -H "Authorization: Bearer ${TOKEN}"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "data.csv",
  "created": "2024-05-14T12:14:33.825316+00:00",
  "updated": "2024-05-14T12:21:13.496989+00:00",
  "status": "completed",
  "metadata": null,
  "version_id": "a60d5e5b-6a98-4df0-ab3d-833f04942f8c",
  "file_id": "cba486b9-a910-4f06-aaa3-f6fb8e37e60b",
  "checksum": "md5:55ec0ec499334e6ad6bf166959d52a1e",
  "bucket_id": "1bc100b6-8730-4ee3-86ec-4015bb8d8dc3",
  "storage_class": "L",
  "size": 124,
  "mimetype": "text/csv",
  "links": {
    "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv",
    "content": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/content",
    "commit": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/files/data.csv/commit"
  }
}
```

### Publish the Draft

Finally, publish the draft to make it a public record.

```bash
curl -i -X POST https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/actions/publish \
     -H "Authorization: Bearer ${TOKEN}"
```

```http
HTTP/1.1 202 ACCEPTED
Content-Type: application/json

{
  "id": "ha4g3-7x208",
  "is_draft": false,
  "is_published": true,
  "status": "published",
  "created": "2024-05-14T12:22:34.225249+00:00",
  "updated": "2024-05-14T12:22:34.344048+00:00",
  "revision_id": 3,
  "metadata": {
    "creators": [
      {
        "affiliations": [{ "name": "Brown University" }],
        "person_or_org": {
          "family_name": "Carberry",
          "given_name": "Josiah",
          "type": "personal",
          "identifiers": [
            { "identifier": "0000-0002-1825-0097", "scheme": "orcid" }
          ],
          "name": "Carberry, Josiah"
        }
      }
    ],
    "resource_type": {
      "id": "dataset",
      "title": { "de": "Datensatz", "en": "Dataset" }
    },
    "publication_date": "2024-05-14",
    "title": "Poltergeist activity readings dataset",
    "publisher": "InvenioRDM"
  },
  "access": {
    "files": "public",
    "record": "public",
    "status": "open",
    "embargo": { "reason": null, "active": false }
  },
  "parent": {
    "access": { "links": [], "owned_by": [{ "user": 25 }] },
    "id": "bhgqt-2ke02",
    "communities": {}
  },
  "pids": {
    "oai": {
      "identifier": "oai:inveniordm.web.cern.ch:ha4g3-7x208",
      "provider": "oai"
    },
    "doi": {
      "identifier": "10.81088/ha4g3-7x208",
      "client": "datacite",
      "provider": "datacite"
    }
  },
  "versions": { "is_latest_draft": true, "index": 1, "is_latest": true },
  "files": { "enabled": true, "order": [] },
  "custom_fields": {},
  "stats": {
    "all_versions": {
      "unique_downloads": 0,
      "data_volume": 0.0,
      "downloads": 0,
      "unique_views": 0,
      "views": 0
    },
    "this_version": {
      "unique_downloads": 0,
      "data_volume": 0.0,
      "downloads": 0,
      "unique_views": 0,
      "views": 0
    }
  },
  "links": {
    "self": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208",
    "self_html": "https://inveniordm.web.cern.ch/records/ha4g3-7x208",
    "self_doi": "https://inveniordm.web.cern.ch/doi/10.81088/ha4g3-7x208",
    "doi": "https://doi.org/10.81088/ha4g3-7x208",
    "self_iiif_manifest": "https://inveniordm.web.cern.ch/api/iiif/record:ha4g3-7x208/manifest",
    "self_iiif_sequence": "https://inveniordm.web.cern.ch/api/iiif/record:ha4g3-7x208/sequence/default",
    "files": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/files",
    "archive": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/files-archive",
    "latest": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/versions/latest",
    "latest_html": "https://inveniordm.web.cern.ch/records/ha4g3-7x208/latest",
    "draft": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft",
    "versions": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/versions",
    "access_links": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/access/links",
    "reserve_doi": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/draft/pids/doi",
    "communities": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/communities",
    "communities-suggestions": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/communities-suggestions",
    "requests": "https://inveniordm.web.cern.ch/api/records/ha4g3-7x208/requests"
  },
}
```

## Conclusion

You have now completed the full sequence of creating a draft, uploading a file, and publishing a record in InvenioRDM using cURL. You can read individual entries for each entity to learn more about the available fields and options.

Happy uploading! 🎉
