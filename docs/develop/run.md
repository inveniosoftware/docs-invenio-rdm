# Run it!

Once the application is installed locally and the services are running, our
application just needs to run. For that, the `run` command is executed.

This time, you can avoid setting the `SITE_HOSTNAME` by using the `--host`
and `--port` flags. Otherwise, `SITE_HOSTNAME` from `invenio.cfg` or from the
environment is used.

``` bash
invenio-cli run
```

``` console
# Summarized output
redis up and running!
postgresql up and running!
es up and running!
Starting celery worker...
Starting up local (development) server...
Instance running!
Visit https://127.0.0.1:5000
```

!!! info "Change the host and port"
    By default, the host is `127.0.0.1` and the port is `5000`. Pass `--host` and `--port`
    to change them e.g., `invenio-cli run --host 127.0.0.2 --port 5001`.

## Use your instance: have fun!

Are we done? Yes, let the fun begin...

### List records

!!! warning "Use the specified host and port"
    Due to CSP, it is important that you use the host and port specified when
    running the API calls. This means `localhost` and `127.0.0.1` are not
    interchangable as they usually are. The default is `127.0.0.1:5000`.

Let's see what is in the instance by querying the API. Using another terminal:

``` bash
curl -k -XGET https://127.0.0.1:5000/api/records | python3 -m json.tool
```
``` json
{
    "aggregations": {
        "access_right": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "open",
                    "doc_count": 100
                }
            ]
        },
        ...
    },
    "hits": {
        "hits": [
            {
                "access": {
                    "access_right": "open",
                    "files": false,
                    "owned_by": [{"user": 1}],
                    "metadata": false,
                    "embargo_date": "2021-02-15"
                },
                "created": "2020-10-12 16:25:20.729095",
                "updated": "2020-10-12 16:25:20.729095",
                "revision_id": 1,
                "conceptid": "5fk5g-mq814",
                "id": "zgxnf-z7n12",
                "links": {
                    "files": "https://127.0.0.1:5000/api/records/zgxnf-z7n12/files",
                    "self": "https://127.0.0.1:5000/api/records/zgxnf-z7n12",
                    "self_html": "https://127.0.0.1:5000/records/zgxnf-z7n12"
                },
                "metadata": {
                    "additional_descriptions": [
                        {
                            "description": "This description has been shortened.",
                            "lang": "eng",
                            "type": "Abstract"
                        }
                    ],
                    "additional_titles": [
                        {
                            "lang": "eng",
                            "title": "a research data management platform",
                            "type": "subtitle"
                        },
                        {
                            "lang": "eng",
                            "title": "White, Contreras and Hill's gallery",
                            "type": "alternativetitle"
                        }
                    ],
                    "contributors": [
                        {
                            "person_or_org": {
                                "given_name": "John",
                                "family_name": "Davis",
                                "type": "personal",
                                "name": "Davis, John"
                            },
                            "role": "rightsholder",
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Tran-Kirby"
                                }
                            ]
                        }
                    ],
                    "creators": [
                        {
                            "person_or_org": {
                                "given_name": "Thomas",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Collins",
                                "type": "personal",
                                "name": "Collins, Thomas"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Campos LLC"
                                }
                            ]
                        },
                        {
                            "person_or_org": {
                                "given_name": "Jeffrey",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Padilla",
                                "type": "personal",
                                "name": "Padilla, Jeffrey"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Mcdaniel, Bowen and Church"
                                }
                            ]
                        }
                    ],
                    "dates": [
                        {
                            "date": "1989-07-06",
                            "description": "Random test date",
                            "type": "other"
                        }
                    ],
                    "description": "This description has been shortened.",
                    "formats": [
                        "application/pdf"
                    ],
                    "funding": [
                        {
                            "funder": {
                                "scheme": "ror",
                                "identifier": "1234",
                                "name": "European Commission"
                            },
                            "award": {
                                "title": "OpenAIRE",
                                "scheme": "openaire",
                                "identifier": ".../246686",
                                "number": "246686"
                            }
                        }
                    ],
                    "languages": ["eng"],
                    "locations": [
                        {
                            "place": "Valday",
                            "identifiers": {
                                "geonames": "12345abcde",
                                "wikidata": "12345abcde"
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [36.1315755, -132.239372]
                            },
                            "description": "Random place on land..."
                        }
                    ],
                    "publisher": "InvenioRDM",
                    "publication_date": "1970-12-05",
                    "references": [
                        {
                            "reference": "Reference to something et al.",
                            "identifier": "0000000114559647",
                            "scheme": "isni"
                        }                    ],
                    "related_identifiers": [
                        {
                            "identifier": "10.9999/rdm.9999988",
                            "relation_type": "requires",
                            "resource_type": {
                                "subtype": "image-photo",
                                "type": "image"
                            },
                            "scheme": "doi"
                        }
                    ],
                    "resource_type": {
                        "subtype": "publication-thesis",
                        "type": "publication"
                    },
                    "rights": [
                        {
                            "rights": "Berkeley Software Distribution 3",
                            "uri": "https://opensource.org/licenses/BSD-3-Clause",
                            "identifier": "BSD-3",
                            "scheme": "BSD-3"
                        }
                    ],
                    "sizes": [
                        "11 pages"
                    ],
                    "subjects": [
                        {
                            "subject": "note",
                            "identifier": "03yrm5c26",
                            "scheme": "ror"
                        }
                    ],
                    "title": "Hicks and Sons's gallery",
                    "version": "v0.0.1"
                }
            },
            ...
        ],
        "total": 25
    },
    "links": {
        "self": "https://127.0.0.1:5000/api/records?page=1&size=25&sort=newest",
        "next": "https://127.0.0.1:5000/api/records?page=2&size=25&sort=newest"
    },
    "sortBy": "newest"
}
```

#### Notes

- The output is shortened for readability and your records will be different because they are generated randomly.
- You can use [jq](https://github.com/stedolan/jq) for color highlighting:

```bash
curl -k -XGET https://127.0.0.1:5000/api/records | jq .
```

### Create records

#### Create a draft

You can create a new record **draft** using the API:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
    "access": {
        "access_right": "open",
        "files": true,
        "owned_by": [
            {
                "user": 1
            }
        ],
        "metadata": false,
        "embargo_date": "2021-02-15"
    },
    "metadata": {
        "creators": [
            {
                "person_or_org": {
                    "family_name": "Collins",
                    "given_name": "Thomas",
                    "identifiers": [
                        {
                            "identifier": "0000-0002-1825-0097",
                            "scheme": "orcid"
                        }
                    ],
                    "name": "Collins, Thomas",
                    "type": "personal"
                },
                "affiliations": [
                    {
                        "identifiers": [
                            {
                                "identifier": "03yrm5c26",
                                "scheme": "ror"
                            }
                        ],
                        "name": "Entity One"
                    }
                ]
            }
        ],
        "description": "A story on how Julio Cesar relates to Gladiator.",
        "publication_date": "2020-06-01",
        "resource_type": {
            "type": "publication",
            "subtype": "publication-article"
        },
        "title": "A Romans story",
        "version": "v0.0.1"
    }
}'
```

#### Publish a draft

To publish it, you can take the `"publish"` link from the response:

```json
"links": {
    "files": "https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/files",
    "publish": "https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/actions/publish",
    "self": "https://127.0.0.1:5000/api/records/jnmmp-51n47/draft",
    "self_html": "https://127.0.0.1:5000/uploads/jnmmp-51n47"
}
```

and `POST` to it:

```bash
curl -k -XPOST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/actions/publish
```

### Get a record

To confirm the record is published, you can search for it:

``` bash
curl -k -XGET https://127.0.0.1:5000/api/records?q=Gladiator | python3 -m json.tool
```

or access it directly using the id from the publish response (e.g. `90xv7-xwd20`):

``` bash
curl -k -XGET https://127.0.0.1:5000/api/records/90xv7-xwd20 | python3 -m json.tool
```

### Use your browser

Alternatively, you can use the web UI.

Navigate to [https://127.0.0.1:5000](https://127.0.0.1:5000) . Note that you might need to accept the SSL exception since it's using a test certificate.
And visit the record page for the newly created record (`self_html` above or just search for it). You will see it has no files associated with it. Let's change that!

### Upload a file to a record

For demonstration purposes, we will attach this scientific photo to our record:

![Very scientific picture of a shiba in autumn](img/jaycee-xie-unsplash-shiba.png)

Photo by <a href="https://unsplash.com/@jayceexie?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Jaycee Xie</a> on <a href="https://unsplash.com/@jayceexie?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a>.

Save it as `leaf_shiba.png` in your current directory.

**First**, we need to work with a draft, so we create one from our published record:

!!! warning "Change the `recid`"
    Change `jnmmp-51n47` in the URLs below for the recid of your record.

```bash
curl -k -XPOST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft
```

**Second**, we start the upload process by initializing the file key:

```bash
curl -k -XPOST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/files -H "Content-Type: application/json" -d '[
  {"key": "leaf_shiba.png"}
]'
```

This "pre-flight" API call will allow us to support third-party source/storage in the future.

**Third**, we now upload the insightful picture by using the `"content"` link returned:

```bash
curl -k -XPUT https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/files/leaf_shiba.png/content -H "Content-Type: application/octet-stream" --data-binary @leaf_shiba.png
```

**Fourth**, we complete the upload process by using the `"commit"` link returned:

```bash
curl -k -XPOST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/files/leaf_shiba.png/commit
```

**Finally**, we publish our updated record:

```bash
curl -k -XPOST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/actions/publish
```

This file can then be previewed on the record page and even downloaded.

## Explore the API

To see what other API calls exist, go to the [API reference section](../reference/rest_api.md).

## Stop it

If you want to temporarily stop the instance, without losing the data that
was generated you can use the `stop` command:

```bash
invenio-cli services stop
```

Check the [Cleanup section](./cleanup.md) if you wish to remove every
reference to InvenioRDM from Docker (containers, images, networks, etc.).
