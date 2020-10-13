# Run it!

Once the application is installed locally and the services are running, our
application just needs to run. For that, the `run` command is executed.

``` bash
invenio-cli run
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

!!! warning "Use 127.0.0.1"
    Due to CSP it is important that you use 127.0.0.1, and not localhost. Unless you set the `SERVER_HOSTNAME` to localhost.

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
                        "buckets": [
                            {
                                "key": "",
                                "doc_count": 1
                            }
                        ]
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
                    "files_restricted": false,
                    "created_by": 1,
                    "owners": [1],
                    "access_right": "open",
                    "metadata_restricted": false
                },
                "created": "2020-10-12 16:25:20.729095",
                "updated": "2020-10-12 16:25:20.729095",
                "revision": 1,
                "id": "zgxnf-z7n12",
                "links": {
                    "self": "https://127.0.0.1:5000/api/records/zgxnf-z7n12",
                    "self_html": "https://127.0.0.1:5000/records/zgxnf-z7n12",
                    "files": "https://127.0.0.1:5000/api/records/zgxnf-z7n12/files",
                    "edit": "https://127.0.0.1:5000/api/records/zgxnf-z7n12/draft"
                },
                "metadata": {
                    "_internal_notes": [
                        {
                            "note": "RDM record",
                            "timestamp": "1981-12-29",
                            "user": "inveniouser"
                        }
                    ],
                    "conceptid": "5fk5g-mq814",
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
                            "role": "RightsHolder",
                            "type": "Personal"
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
                                "Orcid": "0000-0002-1825-0097"
                            },
                            "name": "Christina Wright",
                            "type": "Personal"
                        }
                    ],
                    "dates": [
                        {
                            "description": "Random test date",
                            "start": "1989-07-06",
                            "type": "Other"
                        }
                    ],
                    "descriptions": [
                        {
                            "description": "This description has been shortened.",
                            "lang": "eng",
                            "type": "Abstract"
                        }
                    ],
                    "identifiers": {
                            "DOI": "10.9999/rdm.9999999",
                            "arXiv": "9999.99999"
                    },
                    "language": "eng",
                    "licenses": [
                        {
                            "identifier": "BSD-3",
                            "license": "Berkeley Software Distribution 3",
                            "scheme": "BSD-3",
                            "uri": "https://opensource.org/licenses/BSD-3-Clause"
                        }
                    ],
                    "locations": [
                        {
                            "description": "Random place on land for random coordinates...",
                            "place": "Sector 6",
                            "point": {
                                "lat": 82.3308575,
                                "lon": -129.47999
                            }
                        }
                    ],
                    "publication_date": "1970-12-05",
                    "references": [
                        {
                            "identifier": "9999.99988",
                            "reference_string": "Reference to something et al.",
                            "scheme": "GRID"
                        }
                    ],
                    "related_identifiers": [
                        {
                            "identifier": "10.9999/rdm.9999988",
                            "relation_type": "Requires",
                            "resource_type": {
                                "subtype": "image-photo",
                                "type": "image"
                            },
                            "scheme": "DOI"
                        }
                    ],
                    "resource_type": {
                        "subtype": "publication-thesis",
                        "type": "publication"
                    },
                    "subjects": [
                        {
                            "identifier": "subj-1",
                            "scheme": "no-scheme",
                            "subject": "Romans"
                        }
                    ],
                    "titles": [
                        {
                            "lang": "eng",
                            "title": "Hicks and Sons's gallery",
                            "type": "Other"
                        }
                    ],
                    "version": "v0.0.1"
                }
            },
            ...
        ]
    },
    "links": {
        "self": "https://127.0.0.1/api/records?page=1&size=25&sort=newest"
    }
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

!!! warning "Required `publication_date`"
    Since the August release, it is required to pass a `publication_date`.
    Note its addition below.


```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
    "access": {
        "metadata_restricted": false,
        "files_restricted": false,
        "owners": [1],
        "access_right": "open",
        "created_by": 1
    },
    "metadata": {
        "creators": [
            {
                "name": "Julio Cesar",
                "type": "Personal",
                "given_name": "Julio",
                "family_name": "Cesar",
                "identifiers": {
                    "Orcid": "0000-0002-1825-0097"
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
        "descriptions": [
            {
                "description": "A story on how Julio Cesar relates to Gladiator.",
                "type": "Abstract",
                "lang": "eng"
            }
        ],
        "licenses": [
            {
                "license": "Berkeley Software Distribution 3",
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
        "titles": [
            {
                "title": "A Romans story",
                "type": "Other",
                "lang": "eng"
            }
        ],
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
    "aggregations": {},
    "hits": {
        "hits": [
            {
                "access": {
                    "metadata_restricted": false,
                    "files_restricted": false,
                    "owners": [1],
                    "access_right": "open",
                    "created_by": 1,
                },
                "created": "2020-10-13 17:25:20.654095",
                "id": "jnmmp-51n47",
                "links": {
                    "self": "https://127.0.0.1/api/records/jnmmp-51n47",
                    "self_html": "https://127.0.0.1/records/jnmmp-51n47",
                    "files": "https://127.0.0.1/api/records/jnmmp-51n47/files",
                    "edit": "https://127.0.0.1/api/records/jnmmp-51n47/draft"
                },
                "metadata": {
                    "creators": [
                        {
                            "affiliations": [
                                {
                                    "name": "Entity One",
                                    "identifiers": {
                                        "ror": "03yrm5c26"
                                    }
                                }
                            ],
                            "family_name": "Cesar",
                            "identifiers": {
                                "Orcid": "0000-0002-1825-0097"
                            },
                            "given_name": "Julio",
                            "name": "Julio Cesar",
                            "type": "Personal",
                        }
                    ],
                    "descriptions": [
                        {
                            "description": "A story on how Julio Cesar relates to Gladiator.",
                            "type": "Abstract",
                            "lang": "eng"
                        }
                    ],
                    "licenses": [
                        {
                            "license": "Berkeley Software Distribution 3",
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
                    "titles": [
                        {
                            "title": "A Romans story",
                            "type": "Other",
                            "lang": "eng"
                        }
                    ],
                    "version": "v0.0.1"
                },
                "revision": 1,
                "updated": "2020-10-13 17:25:20.694095"
            }
        ],
        "total": 1
    },
     "links": {
        "self": "https://127.0.0.1/api/records?size=25&page=1&q=Gladiator"
    },
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
