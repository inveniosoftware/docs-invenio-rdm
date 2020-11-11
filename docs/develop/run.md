# Run it!

Once the application is installed locally and the services are running, our
application just needs to run. For that, the `run` command is executed.

This time, you can avoid setting the `SITE_HOSTNAME` by using the `--host`
and `--port` flags. Otherwise, `SITE_HOSTNAME` from `invenio.cfg` or from the
environment is used.

``` bash
invenio-cli run --host 127.0.0.1 --port 5000
```

``` console
# Summarized output
Making sure containers are up...
Starting celery worker...
Starting up local (development) server...
Instance running!
Visit https://127.0.0.1:5000
```

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
        "resource_type": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "publication",
                    "doc_count": 8,
                    "subtype": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "publication-other",
                                "doc_count": 2
                            },
                            {
                                "key": "publication-article",
                                "doc_count": 1
                            },
                            {
                                "key": "publication-deliverable",
                                "doc_count": 1
                            },
                            {
                                "key": "publication-patent",
                                "doc_count": 1
                            },
                            {
                                "key": "publication-report",
                                "doc_count": 1
                            },
                            {
                                "key": "publication-taxonomictreatment",
                                "doc_count": 1
                            },
                            {
                                "key": "publication-thesis",
                                "doc_count": 1
                            }
                        ]
                    }
                },
                {
                    "key": "dataset",
                    "doc_count": 1,
                    "subtype": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": []
                    }
                },
                {
                    "key": "image",
                    "doc_count": 1,
                    "subtype": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "image-photo",
                                "doc_count": 1
                            }
                        ]
                    }
                }
            ]
        },
        "access_right": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "open",
                    "doc_count": 10
                }
            ]
        }
    },
    "hits": {
        "hits": [
            {
                "access": {
                    "access_right": "open",
                    "files": false,
                    "owned_by": [1],
                    "metadata": false,
                    "embargo_date": "2021-02-15"
                },
                "created": "2020-10-12 16:25:20.729095",
                "updated": "2020-10-12 16:25:20.729095",
                "revision_id": 1,
                "conceptid": "5fk5g-mq814",
                "id": "zgxnf-z7n12",
                "links": {
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
                            "affiliations": [
                                {
                                    "identifiers": {
                                        "ror": "03yrm5c26"
                                    },
                                    "name": "Doyle, Miller and Williams"
                                }
                            ],
                            "name": "Gina Brown",
                            "role": "rightsholder",
                            "type": "personal"
                        }
                    ],
                    "creators": [
                        {
                            "affiliations": [
                                {
                                    "identifiers": {
                                        "ror": "03yrm5c26"
                                    },
                                    "name": "Pacheco Ltd",
                                }
                            ],
                            "identifiers": {
                                "orcid": "0000-0002-1825-0097"
                            },
                            "name": "Christina Wright",
                            "type": "personal"
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
                            "identifier": "9999.99988",
                            "reference": "Reference to something et al.",
                            "scheme": "grid"
                        }
                    ],
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
                            "identifier": "subj-1",
                            "scheme": "no-scheme",
                            "subject": "Romans"
                        }
                    ],
                    "title": "Hicks and Sons's gallery",
                    "version": "v0.0.1"
                }
            },
            ...
        ],
        "total": 10
    },
    "links": {
        "self": "https://127.0.0.1:5000/api/records?page=1&size=25&sort=newest"
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

You can create a new record **draft** using the API:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
    "access": {
        "access_right": "open",
        "files": false,
        "owned_by": [1],
        "metadata": false,
        "embargo_date": "2021-02-15"
    },
    "metadata": {
        "creators": [
            {
                "name": "Julio Cesar",
                "type": "personal",
                "given_name": "Julio",
                "family_name": "Cesar",
                "identifiers": {
                    "orcid": "0000-0002-1825-0097"
                },
                "affiliations": [
                    {
                        "name": "Entity One",
                        "identifiers": {
                            "ror": "03yrm5c26"
                        }
                    }
                ]
            }
        ],
        "description": "A story on how Julio Cesar relates to Gladiator.",
        "rights": [
            {
                "rights": "Berkeley Software Distribution 3",
                "uri": "https://opensource.org/licenses/BSD-3-Clause",
                "identifier": "BSD-3",
                "scheme": "BSD-3"
            }
        ],
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

To publish it, you can take the `"publish"` link from the response:

```json
"links": {
    "self": "https://127.0.0.1:5000/api/records/jnmmp-51n47/draft",
    "self_html": "https://127.0.0.1:5000/uploads/jnmmp-51n47",
    "publish": "https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/actions/publish"
}
```

and `POST` to it:

```bash
curl -k -X POST https://127.0.0.1:5000/api/records/jnmmp-51n47/draft/actions/publish
```

And then search for it:

``` bash
curl -k -XGET https://127.0.0.1:5000/api/records?q=Gladiator | python3 -m json.tool
```

``` json
{
    "hits": {
        "hits": [
            {
                "revision_id": 1,
                "updated": "2020-11-10 22:59:47.203708",
                "access": {
                    "access_right": "open",
                    "files": false,
                    "owned_by": [1],
                    "metadata": false,
                    "embargo_date": "2021-02-15"
                },
                "metadata": {
                    "resource_type": {
                        "type": "publication",
                        "subtype": "publication-article"
                    },
                    "description": "A story on how Julio Cesar relates to Gladiator.",
                    "rights": [
                        {
                            "rights": "Berkeley Software Distribution 3",
                            "uri": "https://opensource.org/licenses/BSD-3-Clause",
                            "identifier": "BSD-3",
                            "scheme": "BSD-3"
                        }
                    ],
                    "creators": [
                        {
                            "identifiers": {
                                "orcid": "0000-0002-1825-0097"
                            },
                            "given_name": "Julio",
                            "name": "Julio Cesar",
                            "family_name": "Cesar",
                            "affiliations": [
                                {
                                    "identifiers": {
                                        "ror": "03yrm5c26"
                                    },
                                    "name": "Entity One"
                                }
                            ],
                            "type": "personal"
                        }
                    ],
                    "version": "v0.0.1",
                    "publication_date": "2020-06-01",
                    "title": "A Romans story"
                },
                "id": "90xv7-xwd20",
                "created": "2020-11-10 22:59:47.103850",
                "conceptid": "b2jgw-r0229",
                "links": {
                    "self_html": "https://127.0.0.1:5000/records/90xv7-xwd20",
                    "self": "https://127.0.0.1:5000/api/records/90xv7-xwd20"
                }
            }
        ],
        "total": 1
    },
    "links": {
        "self": "https://127.0.0.1:5000/api/records?page=1&q=Gladiator&size=25&sort=bestmatch"
    },
    "sortBy": "bestmatch",
    "aggregations": {
        "resource_type": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "publication",
                    "doc_count": 1,
                    "subtype": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "publication-article",
                                "doc_count": 1
                            }
                        ]
                    }
                }
            ]
        },
        "access_right": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "open",
                    "doc_count": 1
                }
            ]
        }
    }
}
```

### Use your browser

Alternatively, you can use the web UI.

Navigate to [https://127.0.0.1:5000](https://127.0.0.1:5000) . Note that you might need to accept the SSL exception since it's using a test certificate.
And visit the record page for the newly created record. You will see it has no files associated with it. Let's change that!

### Upload a file to a record

!!! error "Temporarily not supported"
    This is temporarily disabled until the new API is fully compatible with it.

For demonstration purposes, we will attach this scientific photo:

![Very scientific picture of a shiba in the snow](https://images.unsplash.com/photo-1548116137-c9ac24e446c9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80)

by <a href="https://unsplash.com/@matyssik" target="_blank" rel="noopener noreferrer">Ian Matyssik</a>.

Save it as `snow_doge.jpg` in your current directory. Then upload it to the record:

!!! warning "Change the `recid`"
    Change `jnmmp-51n47` in the URLs below for the recid of your record.

``` bash
curl -k -X PUT https://127.0.0.1:5000/api/records/jnmmp-51n47/files/snow_doge.jpg -H "Content-Type: application/octet-stream" --data-binary @snow_doge.jpg
```

This file can then be previewed on the record page and even downloaded.

## Stop it

If you want to temporarily stop the instance, without losing the data that
was generated you can use the `stop` command:

```bash
invenio-cli stop
```

Check the [Cleanup section](./cleanup.md) if you wish to remove every
reference to InvenioRDM from Docker (containers, images, networks, etc.).
