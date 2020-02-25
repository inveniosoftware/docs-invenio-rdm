# Run it!

Once the application is installed locally and the services are running, our
application just needs to run. For that, the `run` command is executed.

``` console
$ invenio-cli run
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

``` console
$ curl -k -XGET https://localhost:5000/api/records/ | python3 -m json.tool
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
                    "doc_count": 10,
                    "key": "image"
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
                            "identifiers": [
                                {
                                    "identifier": "9999-9999-9999-9998",
                                    "scheme": "Orcid"
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
                                    "identifier": "entity-one",
                                    "name": "Pacheco Ltd",
                                    "scheme": "entity-id-scheme"
                                }
                            ],
                            "identifiers": [
                                {
                                    "identifier": "9999-9999-9999-9999",
                                    "scheme": "Orcid"
                                }
                            ],
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
                    "identifiers": [
                        {
                            "identifier": "10.9999/rdm.9999999",
                            "scheme": "DOI"
                        },
                        {
                            "identifier": "9999.99999",
                            "scheme": "arXiv"
                        }
                    ],
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
                                "subtype": "photo",
                                "type": "image"
                            },
                            "scheme": "DOI"
                        }
                    ],
                    "resource_type": {
                        "subtype": "photo",
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
}
```

**Note**: Output shortened for readability. Your records will be different because they are generated randomly.

**Pro Tip**: You can use [jq](https://github.com/stedolan/jq) for color highlighting:

```console
$ curl -k -XGET https://localhost:5000/api/records/ | jq .
...
```

### Create records

You can create a new record using the API:

```console
$ curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '{
    "_access": {
		"metadata_restricted": false,
		"files_restricted": false
	},
	"_owners": [1],
	"_created_by": 1,
	"access_right": "open",
	"resource_type": {
		"type": "image",
		"subtype": "photo"
	},
	"identifiers": [
        {
            "identifier": "10.9999/rdm.9999999",
            "scheme": "DOI"
        }, {
            "identifier": "9999.99999",
            "scheme": "arXiv"
        }
    ],
	"creators": [
        {
            "name": "Julio Cesar",
            "type": "Personal",
            "given_name": "Julio",
            "family_name": "Cesar",
            "identifiers": [
                {
                    "identifier": "9999-9999-9999-9999",
                    "scheme": "Orcid"
                }
            ],
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

``` console
$ curl -k -XGET https://localhost:5000/api/records/?q=Romans | python3 -m json.tool
{
    "aggregations": {
        [...]
    },
    "hits": {
        "hits": [
            {
                "created": "2019-12-19T13:05:48.479895+00:00",
                "id": "pv1dx-rwa61",
                "links": {
                    "self": "https://localhost:5000/api/records/pv1dx-rwa61"
                },
                "metadata": {
                    [...]
                    "titles": [{
                        "title": "A Romans story",
                        "type": "Other",
                        "lang": "eng"
                    }]
                },
                "revision": 0,
                "updated": "2019-12-19T13:05:48.479900+00:00"
            }
        ],
        "total": 1
    },
    "links": {
        "self": "https://localhost:5000/api/records/?sort=bestmatch&q=doge&size=10&page=1"
    }
}
```

### Use your browser

Alternatively, you can use the web UI.

Navigate to https://localhost:5000/ . Note that you might need to accept the SSL exception since it's using a test certificate.
And visit the record page for the newly created record. You will see it has no files associated with it. Let's change that!

### Upload a file to a record

For demonstration purposes, we will attach this scientific photo:

![Very scientific picture of a shiba in the snow](https://images.unsplash.com/photo-1548116137-c9ac24e446c9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80)

By <a href="https://unsplash.com/@matyssik" target="_blank" rel="noopener noreferrer">Ian Matyssik</a>

Save it as `snow_doge.jpg` in your current directory. Then upload it to the record:

!!! warning "Change the `recid`"
    Change `pv1dx-rwa61` in the URLs below for the recid of your record.

```
$ curl -k -X PUT https://localhost:5000/api/records/pv1dx-rwa61/files/snow_doge.jpg -H "Content-Type: application/octet-stream" --data-binary @snow_doge.jpg
```

This file can then be previewed on the record page and even downloaded.

## Stop the instance

We have reached the end of this journey, we are going to stop the instance. Nonetheless you can keep testing and playing around with configurations!

``` console
^C
Stopping server and worker...
Server and worker stopped...
```
