# Configuration

You can configure your InvenioRDM instance to best suit your needs. The `invenio.cfg` file, overrides the `config.py` variables provided by [Invenio modules](https://invenio.readthedocs.io/en/latest/general/bundles.html) and their dependencies. We will use configuring permissions as an example of how to configure your application.

For the purpose of this example, we will only allow super users to create records through the REST API. To do so, we define our own permission policy.

Open the `invenio.cfg` file with your favorite editor. We will use `vim` to avoid `emacs` and other wars ;).

``` bash
vim invenio.cfg
```

Let's add the following to the file:

```python
# imports at the top...
from invenio_rdm_records.permissions import RDMRecordPermissionPolicy
from invenio_records_permissions.generators import SuperUser

# ...

# At the bottom
# Our custom Permission Policy
class MyRecordPermissionPolicy(RDMRecordPermissionPolicy):
    can_create = [SuperUser()]

RECORDS_PERMISSIONS_RECORD_POLICY = MyRecordPermissionPolicy
```

And stop and start the server:

```bash
^C
Stopping server and worker...
Server and worker stopped...
```
``` bash
invenio-cli run
```

!!! warning
    Changes to `invenio.cfg` **MUST** be accompanied by a restart to be picked up. This only restarts the server; it does not destroy any data.

When we set `RECORDS_PERMISSIONS_RECORD_POLICY = MyRecordPermissionPolicy`, we are overriding `RECORDS_PERMISSIONS_RECORD_POLICY` provided by [invenio-records-permissions](https://github.com/inveniosoftware/invenio-records-permissions). You will note that `invenio.cfg` is really just a Python module. How convenient!

**Pro tip** : You can type `can_create = []` to achieve the same effect; any empty permission list only allows super users.

That's it configuration-wise. If we try to create a record through the API, your instance will check if you are a super user before allowing you. The same approach to configuration holds for any other setting you would like to override.

Did the changes work? We are going to try to create a new record:

``` bash
curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '{
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
            "name": "Marcus Junius Brutus",
            "type": "Personal",
            "given_name": "Marcus",
            "family_name": "Brutus",
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
            "title": "A permission story",
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

As you can see, the server could not know if we are authenticated/superuser and rejected us:

``` json
{
    "message": "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
    "status": 401
}
```

!!!todo
    Document how to generate an API token when permissions via token work.

Revert the changes in `invenio.cfg` and restart the server to get back to where we were.