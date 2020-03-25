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
Visit https://localhost:5000
```

## Use your instance: have fun!

Are we done? Yes, let the fun begin...

### List records

Let's see what is in the instance by querying the API. Using another terminal:

``` bash
curl -k -XGET https://localhost:5000/api/records/ | python3 -m json.tool
```
``` json
{
    "aggregations": {
        "access_right": {
            "buckets": [
                {
                    "doc_count": 10,
                    "key": "open"
                }
            ],
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0
        },
        "resource_type": {
            "buckets": [
                {
                    "doc_count": 4,
                    "key": "book"
                },
                {
                    "doc_count": 3,
                    "key": "text"
                },
                {
                    "doc_count": 1,
                    "key": "image"
                },
                {
                    "doc_count": 1,
                    "key": "multimedia"
                },
                {
                    "doc_count": 1,
                    "key": "periodical"
                }
            ],
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0
        }
    },
    "hits": {
        "hits": [
            {
                "created": "2020-02-25T15:54:52.127129+00:00",
                "updated": "2020-02-25T15:54:52.127134+00:00",
                "revision": 0,
                "id": "zgxnf-z7n12",
                "links": {
                    "files": "https://localhost:5000/api/records/zgxnf-z7n12/files",
                    "self": "https://localhost:5000/api/records/zgxnf-z7n12"
                },
                "metadata": {
                    "_access": {
                        "files_restricted": false,
                        "metadata_restricted": false
                    },
                    "_created_by": 2,
                    "_default_preview": "previewer one",
                    "_internal_notes": [
                        {
                            "note": "RDM record",
                            "timestamp": "1981-12-29",
                            "user": "inveniouser"
                        }
                    ],
                    "_owners": [1],
                    "access_right": "open",
                    "community": {
                        "primary": "Maincom",
                        "secondary": ["Subcom One", "Subcom Two"]
                    },
                    "contact": "info@inveniosoftware.org",
                    "contributors": [
                        {
                            "affiliations": [
                                {
                                    "identifier": "entity-one",
                                    "name": "Doyle, Miller and Williams",
                                    "scheme": "entity-id-scheme"
                                }
                            ],
                            "identifiers": {
                                "Orcid": "9999-9999-9999-9998"
                            },
                            "name": "Gina Brown",
                            "role": "RightsHolder",
                            "type": "Personal"
                        }
                    ],
                    "creators": [
                        {
                            "affiliations": [
                                {
                                    "identifier": "entity-one",
                                    "name": "Pacheco Ltd",
                                    "scheme": "entity-id-scheme"
                                }
                            ],
                            "identifiers": {
                                "Orcid": "9999-9999-9999-9999"
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
                    "embargo_date": "1997-12-01",
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
                    "recid": "zgxnf-z7n12",
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
                        "subtype": "image-photo",
                        "type": "image"
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
    }
}
```

**Note**: Output shortened for readability. Your records will be different because they are generated randomly.

**Pro Tip**: You can use [jq](https://github.com/stedolan/jq) for color highlighting:

```bash
curl -k -XGET https://localhost:5000/api/records/ | jq .
```

### Create records

You can create a new record using the API:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '{
    "_access": {
        "metadata_restricted": false,
        "files_restricted": false
    },
    "_owners": [1],
    "_created_by": 1,
    "access_right": "open",
    "resource_type": {
        "type": "publication",
        "subtype": "publication-article"
    },
    "identifiers": {
        "DOI": "10.9999/rdm.9999999",
        "arXiv": "9999.99999"
    },
    "creators": [
        {
            "name": "Julio Cesar",
            "type": "Personal",
            "given_name": "Julio",
            "family_name": "Cesar",
            "identifiers": {
                "Orcid": "9999-9999-9999-9999"
            },
            "affiliations": [
                {
                    "name": "Entity One",
                    "identifier": "entity-one",
                    "scheme": "entity-id-scheme"
                }
            ]
        }
    ],
    "titles": [
        {
            "title": "A Romans story",
            "type": "Other",
            "lang": "eng"
        }
    ],
    "descriptions": [
        {
            "description": "A story on how Julio Cesar relates to Gladiator.",
            "type": "Abstract",
            "lang": "eng"
        }
    ],
    "community": {
        "primary": "Maincom",
        "secondary": ["Subcom One", "Subcom Two"]
    },
    "licenses": [
        {
            "license": "Berkeley Software Distribution 3",
            "uri": "https://opensource.org/licenses/BSD-3-Clause",
            "identifier": "BSD-3",
            "scheme": "BSD-3"
        }
    ]
}'
```

And then search for it:

``` bash
curl -k -XGET https://localhost:5000/api/records/?q=Gladiator | python3 -m json.tool
```
``` json
{
    "aggregations": {
        "access_right": {
            "buckets": [
                {
                    "doc_count": 1,
                    "key": "open"
                }
            ],
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0
        },
        "resource_type": {
            "buckets": [
                {
                    "doc_count": 1,
                    "key": "publication"
                }
            ],
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0
        }
    },
    "hits": {
        "hits": [
            {
                "created": "2020-02-26T15:46:55.000116+00:00",
                "id": "8wtcp-1bs44",
                "links": {
                    "files": "https://localhost:5000/api/records/8wtcp-1bs44/files",
                    "self": "https://localhost:5000/api/records/8wtcp-1bs44"
                },
                "metadata": {
                    "_access": {
                        "files_restricted": false,
                        "metadata_restricted": false
                    },
                    "_created_by": 1,
                    "_owners": [
                        1
                    ],
                    "access_right": "open",
                    "community": {
                        "primary": "Maincom",
                        "secondary": [
                            "Subcom One",
                            "Subcom Two"
                        ]
                    },
                    "creators": [
                        {
                            "affiliations": [
                                {
                                    "identifier": "entity-one",
                                    "name": "Entity One",
                                    "scheme": "entity-id-scheme"
                                }
                            ],
                            "family_name": "Cesar",
                            "given_name": "Julio",
                            "identifiers": {
                                "Orcid": "9999-9999-9999-9999"
                            },
                            "name": "Julio Cesar",
                            "type": "Personal"
                        }
                    ],
                    "descriptions": [
                        {
                            "description": "A story on how Julio Cesar relates to Gladiator.",
                            "lang": "eng",
                            "type": "Abstract"
                        }
                    ],
                    "identifiers": {
                        "DOI": "10.9999/rdm.9999999",
                        "arXiv": "9999.99999"
                    },
                    "licenses": [
                        {
                            "identifier": "BSD-3",
                            "license": "Berkeley Software Distribution 3",
                            "scheme": "BSD-3",
                            "uri": "https://opensource.org/licenses/BSD-3-Clause"
                        }
                    ],
                    "publication_date": "2020-02-26",
                    "recid": "8wtcp-1bs44",
                    "resource_type": {
                        "subtype": "publication-article",
                        "type": "publication"
                    },
                    "titles": [
                        {
                            "lang": "eng",
                            "title": "A Romans story",
                            "type": "Other"
                        }
                    ]
                },
                "revision": 0,
                "updated": "2020-02-26T15:46:55.000119+00:00"
            }
        ],
        "total": 1
    },
    "links": {
        "self": "https://localhost:5000/api/records/?sort=bestmatch&q=Gladiator&size=10&page=1"
    }
}
```

### Use your browser

Alternatively, you can use the web UI.

Navigate to [https://localhost:5000](https://localhost:5000) . Note that you might need to accept the SSL exception since it's using a test certificate.
And visit the record page for the newly created record. You will see it has no files associated with it. Let's change that!

### Upload a file to a record

For demonstration purposes, we will attach this scientific photo:

![Very scientific picture of a shiba in the snow](https://images.unsplash.com/photo-1548116137-c9ac24e446c9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80)

by <a href="https://unsplash.com/@matyssik" target="_blank" rel="noopener noreferrer">Ian Matyssik</a>.

Save it as `snow_doge.jpg` in your current directory. Then upload it to the record:

!!! warning "Change the `recid`"
    Change `pv1dx-rwa61` in the URLs below for the recid of your record.

``` bash
curl -k -X PUT https://localhost:5000/api/records/pv1dx-rwa61/files/snow_doge.jpg -H "Content-Type: application/octet-stream" --data-binary @snow_doge.jpg
```

This file can then be previewed on the record page and even downloaded.
