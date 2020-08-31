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

Let's see what is in the instance by querying the API. Note that localhost and 127.0.0.1 can
be used interchangeably. Using another terminal:

!!! warning "New API endpoints"
    The new implementation of the backend is available through the `/api/rdm-records` endpoint.
    Please crosscheck if you are using already crafted requests.

``` bash
curl -k -XGET https://127.0.0.1:5000/api/rdm-records | python3 -m json.tool
```
``` json
{
    "aggregations": {},
    "hits": {
        "hits": [
            {
                "created": "2020-02-25T15:54:52.127129+00:00",
                "updated": "2020-02-25T15:54:52.127134+00:00",
                "revision": 0,
                "pid": "zgxnf-z7n12",
                "links": {
                    "self": "https://127.0.0.1:5000/api/rdm-records/zgxnf-z7n12",
                    "self_html": "https://127.0.0.1:5000/records/zgxnf-z7n12",
                    "files": "https://127.0.0.1:5000/api/rdm-records/zgxnf-z7n12/files",
                    "edit": "https://127.0.0.1:5000/api/rdm-records/zgxnf-z7n12/draft"
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
                    "_publication_date_search": "2020-08-31",
                    "access_right": "open",
                    "conceptrecid": "5fk5g-mq814",
                    "contact": "info@inveniosoftware.org",
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
    },
    "links": {
        "self": "https://127.0.0.1/api/rdm-records?size=25&page=1",
        "next": "https://127.0.0.1/api/rdm-records?size=25&page=2"
    }
}
```

#### Notes

- The output is shortened for readability and your records will be different because they are generated randomly.
- We did the hard work of fully switching to the new API at the cost of temporarily disabling aggregations.
  They will be back in the next release!
- `"links"` have been added!
- You can use [jq](https://github.com/stedolan/jq) for color highlighting:

    ```bash
    curl -k -XGET https://127.0.0.1:5000/api/rdm-records | jq .
    ```

### Create records

You can create a new record **draft** using the API:

!!! warning "Required `publication_date`"
    Since the August release, it is required to pass a `publication_date`.
    Note its addition below.


```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/rdm-records -d '{
    "_access": {
        "metadata_restricted": false,
        "files_restricted": false
    },
    "_created_by": 1,
    "_owners": [1],
    "access_right": "open",
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
    "identifiers": {
        "DOI": "10.9999/rdm.9999999",
        "arXiv": "9999.99999"
    },
    "licenses": [
        {
            "license": "Berkeley Software Distribution 3",
            "uri": "https://opensource.org/licenses/BSD-3-Clause",
            "identifier": "BSD-3",
            "scheme": "BSD-3"
        }
    ],
    "publication_date": "2020-08-31",
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
}'
```

To publish it, you can take the `"publish"` link from the response:

```json
"links": {
    "self": "https://127.0.0.1:5000/api/rdm-records/jnmmp-51n47/draft",
    "self_html": "https://127.0.0.1:5000/deposits/jnmmp-51n47/edit",
    "publish": "https://127.0.0.1:5000/api/rdm-records/jnmmp-51n47/draft/actions/publish"
}
```

and `POST` to it:

```bash
curl -k -X POST https://127.0.0.1:5000/api/rdm-records/jnmmp-51n47/draft/actions/publish
```

And then search for it:

``` bash
curl -k -XGET https://127.0.0.1:5000/api/rdm-records?q=Gladiator | python3 -m json.tool
```
``` json
{
    "aggregations": {},
    "hits": {
        "hits": [
            {
                "created": "2020-02-26T15:46:55.000116+00:00",
                "pid": "jnmmp-51n47",
                "links": {
                    "self": "https://127.0.0.1/api/rdm-records/jnmmp-51n47",
                    "self_html": "https://127.0.0.1/records/jnmmp-51n47",
                    "files": "https://127.0.0.1/api/rdm-records/jnmmp-51n47/files",
                    "edit": "https://127.0.0.1/api/rdm-records/jnmmp-51n47/draft"
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
                    "creators": [
                        {
                            "affiliations": [
                                {
                                    "identifiers": {
                                        "ror": "03yrm5c26"
                                    },
                                    "name": "Entity One"
                                }
                            ],
                            "family_name": "Cesar",
                            "given_name": "Julio",
                            "identifiers": {
                                "Orcid": "0000-0002-1825-0097"
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
                    "pid": "jnmmp-51n47",
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
        "self": "https://127.0.0.1/api/rdm-records?size=25&page=1&q=Gladiator",
        "next": "https://127.0.0.1/api/rdm-records?size=25&page=2&q=Gladiator"
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
curl -k -X PUT https://127.0.0.1:5000/api/rdm-records/jnmmp-51n47/files/snow_doge.jpg -H "Content-Type: application/octet-stream" --data-binary @snow_doge.jpg
```

This file can then be previewed on the record page and even downloaded.
