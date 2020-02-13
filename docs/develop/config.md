# Configuration

You can configure your InvenioRDM instance to best suit your needs. The `invenio.cfg` file, overrides the `config.py` variables provided by [Invenio modules](https://invenio.readthedocs.io/en/latest/general/bundles.html) and their dependencies. We will use configuring permissions as an example of how to configure your application.

For the purpose of this example, we will only allow super users to create records through the REST API. To do so, we define our own permission policy.

Open the `invenio.cfg` file with your favorite editor. We will use `vim` to avoid `emacs` and other wars ;).

``` console
$ vim invenio.cfg
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

When we set `RECORDS_PERMISSIONS_RECORD_POLICY = MyRecordPermissionPolicy`, we are overriding `RECORDS_PERMISSIONS_RECORD_POLICY` provided by [invenio-records-permissions](https://github.com/inveniosoftware/invenio-app-rdm). You will note that `invenio.cfg` is really just a Python module. How convenient!

**Pro tip** : You can type `can_create = []` to achieve the same effect; any empty permission list only allows super users.

That's it configuration-wise. If we try to create a record through the API, your instance will check if you are a super user before allowing you. The same approach to configuration holds for any other setting you would like to override.

Did the changes work? We are going to try to create a new record:

``` console
$ curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '
{
    "access": {
        "metadata_restricted": "false",
        "files_restricted": "false"
    },
    "access_right": "open",
    "contributors": [{"name": "Jon Doe"}],
    "description": "A Holiday Record description",
    "owners": [1],
    "publication_date": "25/12/2019",
    "resource_type": {
        "type": "Dataset",
        "subtype": "dataset"
    },
    "title": "A Holiday Record"
}'
```

As you can see, the server could not know if we are authenticated/superuser and rejected us:

``` console
{"message":"The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.","status":401}
```

**Advanced example**:

1- Create a user, for example using the web UI (*sign up* button). Alternatively, you can do so with the CLI, executing the following command (Wait until you read point number *2* before executing):

``` console
pipenv run invenio users create user@test.ch --password=123456
```

Note that the user will have ID 1 if it was the first one created.

2- Grant admin access to it. In order to do so, we only have to add the `-a` flag to the previous command:

``` console
pipenv run invenio users create admin@test.ch -a --password=123456
```

Note that this user will have ID 2.

3- Get a token and try to create the record again. You can do so on the UI by going to `settings->applications-->new token`. Alternatively you can do it in the terminal by executing the following command:

``` console
# TODO Wait until invenio-oauthclient REST only is integrated
```

Afterwards we can test if the new permissions are working correctly.

``` console
$ curl -k -XPOST -H "Authorization:Bearer sHHq1K9y7a2v5doKDRSFmSFOxa1tZDHFcbs31npaxm1sFEt27yomLMt0ynkl" -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '
{
    "access": {
        "metadata_restricted": "false",
        "files_restricted": "false"
    },
    "access_right": "open",
    "contributors": [{"name": "Jon Doe"}],
    "description": "A Holiday Record description",
    "owners": [1],
    "publication_date": "25/12/2019",
    "resource_type": {
        "type": "Dataset",
        "subtype": "dataset"
    },
    "title": "A Holiday Record"
}'
```

It works!
