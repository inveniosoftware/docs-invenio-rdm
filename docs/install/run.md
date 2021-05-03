# Use InvenioRDM

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
        }
    },
    "hits": {
        "hits": [
            {
                "access": {
                    "files": "restricted",
                    "embargo": {
                        "reason": "top secret material",
                        "until": "2021-08-09",
                        "active": true
                    },
                    "record": "public",
                    "owned_by": [
                        {
                            "user": 1
                        }
                    ]
                },
                "id": "mrewd-axc44",
                "metadata": {
                    "sizes": [
                        "11 pages"
                    ],
                    "references": [
                        {
                            "identifier": "0000000114559647",
                            "scheme": "isni",
                            "reference": "Reference to something et al."
                        }
                    ],
                    "additional_descriptions": [
                        {
                            "lang": "eng",
                            "description": "The ten free worry lose receive. Feeling church know anyone significant. Public note part style want discussion.",
                            "type": "methods"
                        },
                        {
                            "lang": "eng",
                            "description": "Make voice store worry artist real. Ever movement policy born.\nAlmost trial new if. Keep someone keep light heavy indicate.\nSon improve both. Budget home mean evidence crime by.",
                            "type": "methods"
                        }
                    ],
                    "funding": [
                        {
                            "funder": {
                                "identifier": "03yrm5c26",
                                "scheme": "ror",
                                "name": "European Commission"
                            },
                            "award": {
                                "identifier": "0000-0002-1825-0097",
                                "scheme": "orcid",
                                "number": "246686",
                                "title": "OpenAIRE"
                            }
                        }
                    ],
                    "formats": [
                        "application/pdf"
                    ],
                    "creators": [
                        {
                            "person_or_org": {
                                "type": "personal",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Mercado",
                                "given_name": "Jessica",
                                "name": "Mercado, Jessica"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Harris-Grimes"
                                }
                            ]
                        },
                        {
                            "person_or_org": {
                                "type": "personal",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Arnold",
                                "given_name": "Rebecca",
                                "name": "Arnold, Rebecca"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Miller-Smith"
                                }
                            ]
                        },
                        {
                            "person_or_org": {
                                "type": "personal",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Lara",
                                "given_name": "Sherri",
                                "name": "Lara, Sherri"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Jensen-Dunn"
                                }
                            ]
                        },
                        {
                            "person_or_org": {
                                "type": "personal",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0002-1825-0097",
                                        "scheme": "orcid"
                                    }
                                ],
                                "family_name": "Garcia",
                                "given_name": "Steven",
                                "name": "Garcia, Steven"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Hernandez Group"
                                }
                            ]
                        }
                    ],
                    "resource_type": {
                        "type": "publication"
                    },
                    "publication_date": "1971-12/1973-06-22",
                    "publisher": "InvenioRDM",
                    "additional_titles": [
                        {
                            "lang": "eng",
                            "type": "subtitle",
                            "title": "a research data management platform"
                        },
                        {
                            "lang": "eng",
                            "type": "alternativetitle",
                            "title": "Anderson and Sons's gallery"
                        }
                    ],
                    "version": "v0.0.1",
                    "contributors": [
                        {
                            "role": "rightsholder",
                            "person_or_org": {
                                "type": "personal",
                                "family_name": "Cruz",
                                "given_name": "Ashley",
                                "name": "Cruz, Ashley"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Clark-Garrett"
                                }
                            ]
                        },
                        {
                            "role": "rightsholder",
                            "person_or_org": {
                                "type": "personal",
                                "family_name": "Peck",
                                "given_name": "Abigail",
                                "name": "Peck, Abigail"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Barnes, Hall and Ramos"
                                }
                            ]
                        },
                        {
                            "role": "rightsholder",
                            "person_or_org": {
                                "type": "personal",
                                "family_name": "Davies",
                                "given_name": "Karen",
                                "name": "Davies, Karen"
                            },
                            "affiliations": [
                                {
                                    "identifiers": [
                                        {
                                            "identifier": "03yrm5c26",
                                            "scheme": "ror"
                                        }
                                    ],
                                    "name": "Russell and Sons"
                                }
                            ]
                        }
                    ],
                    "subjects": [
                        {
                            "identifier": "03yrm5c26",
                            "scheme": "ror",
                            "subject": "child"
                        },
                        {
                            "identifier": "03yrm5c26",
                            "scheme": "ror",
                            "subject": "strategy"
                        }
                    ],
                    "description": "Picture risk field article. Do meeting measure nothing option drug. Marriage test evidence. Whole will paper give thing task.\nLawyer music hard report game generation answer rock. Window great surface piece involve lay all. Hour far great he close when official surface......",
                    "title": "Howard LLC's gallery"
                },
                "created": "2021-02-26 10:28:02.245807",
                "updated": "2021-02-26 10:28:02.261941",
                "published": true,
                "status": "published",
                "conceptid": "62fe3-3t414",
                "revision_id": 1,
                "links": {
                    "files": "https://127.0.0.1:5000/api/records/mrewd-axc44/files",
                    "self": "https://127.0.0.1:5000/api/records/mrewd-axc44",
                    "self_html": "https://127.0.0.1:5000/records/mrewd-axc44"
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

!!! info "Authentication required"

    All requests to the create-related REST API endpoints require authentication.

#### Create a draft

You can create a new record **draft** using the API:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
"access": {
    "record": "public",
    "files": "public"
},
"metadata": {
    "publication_date": "2020-06-01",
    "resource_type": {
        "type": "image",
        "subtype": "image-photo"
    },
    "creators": [
        {
            "person_or_org": {
                "family_name": "Brown",
                "given_name": "Troy",
                "type": "personal"
            }
        },
        {
            "person_or_org": {
                "name": "Troy Inc.",
                "type": "organizational"
            }
        }
    ],
    "title": "A Romans story"
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




### List communities

Similar to listing the records, let's list communities in the instance by querying the API. In a separate terminal:

``` bash
curl -k -XGET https://127.0.0.1:5000/api/communities | jq
```
``` json
{ 
  "hits": {
    "hits": [
        {
        "revision_id": 3,
        "id": "new_community_id",
        "metadata": {
            "page": "Information for my community.",
            "funding": [
            {
                "funder": {
                "name": "European Commission",
                "identifier": "00k4n6c32",
                "scheme": "ror"
                },
                "award": {
                "identifier": ".../246686",
                "number": "246686",
                "scheme": "openaire",
                "title": "OpenAIRE"
                }
            }
            ],
            "type": "event",
            "title": "My Community",
            "organizations": [
            {
                "name": "CERN",
                "identifiers": [
                {
                    "identifier": "01ggx4157",
                    "scheme": "ror"
                }
                ]
            }
            ],
            "description": "This is an example Community.",
            "curation_policy": "This is the kind of records we accept.",
            "website": "https://inveniosoftware.org/"
        },
        "links": {
            "self": "https://127.0.0.1:5000/api/communities/new_community_id",
            "self_html": "https://127.0.0.1:5000/communities/new_community_id",
            "settings_html": "https://127.0.0.1:5000/communities/new_community_id/settings",
            "logo": "https://127.0.0.1:5000/api/communities/new_community_id/logo",
            "rename": "https://127.0.0.1:5000/api/communities/new_community_id/rename"
        },
        "created": "2021-04-29T15:02:07.838322+00:00",
        "access": {
            "member_policy": "open",
            "owned_by": [
            {
                "user": 2
            }
            ],
            "visibility": "public",
            "record_policy": "open"
        },
        "updated": "2021-04-29T15:02:24.532559+00:00"
        },
        {
        "revision_id": 2,
        "id": "commnew",
        "metadata": {
            "title": "New Comm"
        },
        "links": {
            "self": "https://127.0.0.1:5000/api/communities/commnew",
            "self_html": "https://127.0.0.1:5000/communities/commnew",
            "settings_html": "https://127.0.0.1:5000/communities/commnew/settings",
            "logo": "https://127.0.0.1:5000/api/communities/commnew/logo",
            "rename": "https://127.0.0.1:5000/api/communities/commnew/rename"
        },
        "created": "2021-04-29T14:18:56.552252+00:00",
        "access": {
            "member_policy": "open",
            "owned_by": [
            {
                "user": 2
            }
            ],
            "visibility": "public",
            "record_policy": "open"
        },
        "updated": "2021-04-29T14:18:56.577770+00:00"
        },
        {
        "revision_id": 2,
        "id": "comm_id",
        "metadata": {
            "type": "topic",
            "title": "Title"
        },
        "links": {
            "self": "https://127.0.0.1:5000/api/communities/comm_id",
            "self_html": "https://127.0.0.1:5000/communities/comm_id",
            "settings_html": "https://127.0.0.1:5000/communities/comm_id/settings",
            "logo": "https://127.0.0.1:5000/api/communities/comm_id/logo",
            "rename": "https://127.0.0.1:5000/api/communities/comm_id/rename"
        },
        "created": "2021-04-29T14:06:30.830609+00:00",
        "access": {
            "member_policy": "open",
            "owned_by": [
            {
                "user": 2
            }
            ],
            "visibility": "public",
            "record_policy": "open"
        },
        "updated": "2021-04-29T14:06:30.853746+00:00"
        },
        {
        "revision_id": 2,
        "id": "foster-anderson",
        "metadata": {
            "page": "Star whom top enter measure real interview. Style company prevent detail federal cultural generation. Carry southern travel.\nBring any job prove. Agreement create whatever often house deal month kitchen.\nNatural rate why near three both particular.\nYourself low force prevent have story push. Open woman relate standard receive.",
            "funding": [
            {
                "funder": {
                "name": "European Commission",
                "identifier": "03yrm5c26",
                "scheme": "ror"
                },
                "award": {
                "identifier": "0000-0002-1825-0097",
                "number": "246686",
                "scheme": "orcid",
                "title": "OpenAIRE"
                }
            }
            ],
            "type": "topic",
            "title": "Year say region.",
            "organizations": [
            {
                "name": "CERN",
                "identifiers": [
                {
                    "identifier": "01ggx4157",
                    "scheme": "ror"
                }
                ]
            }
            ],
            "description": "Fact decision director set former follow. Method study traditional. Would lawyer hundred.\nOwn board team ahead eight. Cause enough blood produce send impact enter security. Go piece market allow region.\nOut imagine think.\nLay environment prepare star.\nDuring drop eye eat prepare loss. Service you phone chair teach government peace your. Leader low room serve for.\nFood cup report stop edge scientist use lot. But image here hard. Result strategy window available read kitchen interesting.\nLong paper look avoid know seem political.\nNorth control exactly seat five couple specific you. Discuss claim campaign not green should order. Ground enough exist against send show.\nNatural talk morning board. Teach early still management series according teacher cup. Arm international message prepare. At two hear clear.",
            "curation_policy": "Exactly executive well he. Put your best open education find.\nNot international animal rich full race. Choose spring success daughter. Enter five describe it knowledge fund seat.\nOperation open garden agency. Professor story happy area serve discussion position director.\nPretty can event any carry across. Civil sit again better expect according product. Upon environment car hear only. Phone probably wife toward along.",
            "website": "https://shea.org"
        },
        "links": {
            "self": "https://127.0.0.1:5000/api/communities/foster-anderson",
            "self_html": "https://127.0.0.1:5000/communities/foster-anderson",
            "settings_html": "https://127.0.0.1:5000/communities/foster-anderson/settings",
            "logo": "https://127.0.0.1:5000/api/communities/foster-anderson/logo",
            "rename": "https://127.0.0.1:5000/api/communities/foster-anderson/rename"
        },
        "created": "2021-04-29T13:07:06.996160+00:00",
        "access": {
            "member_policy": "closed",
            "owned_by": [],
            "visibility": "public",
            "record_policy": "open"
        },
        "updated": "2021-04-29T13:07:07.014840+00:00"
        }
    ],
    "total": 65
    },
    "sortBy": "newest",
    "aggregations": {
    "domain": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": []
    },
    "type": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
        {
            "key": "organization",
            "doc_count": 21
        },
        {
            "key": "event",
            "doc_count": 20
        },
        {
            "key": "topic",
            "doc_count": 13
        },
        {
            "key": "project",
            "doc_count": 10
        }
        ]
      }
    },
    "links": {
    "self": "https://127.0.0.1:5000/api/communities?page=1&size=25&sort=newest",
    "next": "https://127.0.0.1:5000/api/communities?page=2&size=25&sort=newest"
    }
  }
}
```

#### Notes
- Results are abbreviated for ease of reading.
- [jq](https://github.com/stedolan/jq) is for pretty formating and coloring.


### Create communities

!!! info "Authentication required"

    All requests to the create-related REST API endpoints require authentication.

#### Create a community

You can create a new community using the API:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/communities?access_token=<token> -d '{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open"
  },
  "id": "yet_another_community",
  "metadata": {
    "title": "Awesome Repositories Conf 2021",
    "description": "Awesome Repositories Confereans is organized by those who desire to give researchers insigth in how to build up their research repositories, how to keep it tidy and organized aiming maximum reusablitiy and reproducibilty of their research.",
    "type": "event",
    "curation_policy": "We accept Zenodo, GitHub, GitLab, Elsevier and Arvix kind of records with a source repository along with a detailed explanition of each file/directory in it. If exists, datasets should be referenced and their schema should be explained in detail. In addition, there should be one main report explainind the entire workflow.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/"
  }
}'
```

#### Update a community

You can update a community's profile and access settings using the API:

```bash
curl -k -XPUT -H "Content-Type: application/json" https://127.0.0.1:5000/api/communities/yet_another_community?access_token=<token> -d '{
  "access": {
    "visibility": "restricted",
    "member_policy": "open",
    "record_policy": "open"
  },
  "id": "yet_another_community",
  "metadata": {
    "title": "Awesome Repositories Conference 2021"
  }
}'
```

### Rename a community

You can rename a community using the API: 

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/communities/yet_another_community/rename?access_token=<token> -d '{
  "access": {
    "visibility": "restricted",
  },
  "id": "AwesomeRepo21",
  "metadata": {
    "title": "Awesome Repositories Conference 2021"
  }
}'
```

### Get a community

You can get a community using the API as long as `id` is known. 

```bash
curl -k -XGET -H "Content-Type: application/json" https://127.0.0.1:5000/api/comm_id?access_token=<token>
```

### Update community logo

You can update a community logo using the API.

```bash
curl -k -XPUT -H "Content-Type: application/octet-stream" https://127.0.0.1:5000/api/communities/new_community_id/logo?access_token=<token> -d logo.jpg

```

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
