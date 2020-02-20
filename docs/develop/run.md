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
                    "key": "Dataset"
                }
            ],
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0
        }
    },
    "hits": {
        "hits": [
            {
                "created": "2019-12-19T20:15:29.167218+00:00",
                "id": "s2pwq-mzw48",
                "links": {
                    "files": "https://localhost:5000/api/records/s2pwq-mzw48/files",
                    "self": "https://localhost:5000/api/records/s2pwq-mzw48"
                },
                "metadata": {
                    "_access": {
                        "files_restricted": false,
                        "metadata_restricted": false
                    },
                    "access_right": "open",
                    "contributors": [
                        {
                            "name": "Jeanne Jones"
                        }
                    ],
                    "description": "repurpose robust eyeballs",
                    "owners": [
                        1
                    ],
                    "publication_date": "2009-12-30",
                    "recid": "s2pwq-mzw48",
                    "resource_type": {
                        "subtype": "dataset",
                        "type": "Dataset"
                    },
                    "title": "Rodriguez Group's dataset"
                },
                "revision": 0,
                "updated": "2019-12-19T20:15:29.167224+00:00"
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
$ curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '
{
    "access": {
        "metadata_restricted": "false",
        "files_restricted": "false"
    },
    "access_right": "open",
    "contributors": [{"name": "Jon Doe"}, {"name": "Ian Matyssik"}],
    "description": "Photo-analysis of doge in crystalline structures",
    "owners": [1],
    "publication_date": "05/11/2019",
    "resource_type": {
        "type": "image",
        "subtype": "photo"
    },
    "title": "Manually indexed record"
}'
```

And then search for it:

``` console
$ curl -k -XGET https://localhost:5000/api/records/?q=doge | python3 -m json.tool
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
                    "title": "Manually indexed record"
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
