## Define a custom controlled vocabulary

InvenioRDM deals with many controlled vocabularies. And since agreeing on standard
vocabularies is notoriously difficult, InvenioRDM allows you to use the controlled
vocabularies **you** want. Here we show how to customize your resource types vocabulary,
but the same approach holds true for any other vocabulary.

We start by copying [the default resource types vocabulary file](https://github.com/inveniosoftware/invenio-rdm-records/raw/master/invenio_rdm_records/vocabularies/resource_types.csv)
and modifying it with our own vocabulary entries. Make sure to keep the same headers!

!!! info "Use the hierarchy to your advantage"
    You will notice the hierarchy in the default file. It reduces repetition and makes sections visually clear. You can use that pattern for your own entries too.

Save this file in the `app_data/vocabularies/` folder. We call ours `resource_types.csv`. Very original!
Then edit `invenio.cfg` to tell InvenioRDM to use this file.

```python
# imports at the top...
from os.path import abspath, dirname, join

# ... content of the invenio.cfg file omitted for brevity ...

# At the bottom
# Our custom Vocabularies
RDM_RECORDS_CUSTOM_VOCABULARIES = {
    'resource_type': {  # Pre-defined key. See note below
        'path': join(
            dirname(abspath(__file__)),
            'app_data', 'vocabularies', 'resource_types.csv'
        )
    }
}
```

!!! info "Other vocabularies"
    See the [Vocabulary source code](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/vocabularies/__init__.py)
    in invenio-rdm-records to know the keys for all supported vocabularies.

Restart your server and your vocabulary will now be used for resource types!


## Extend the metadata model

!!! error "Temporarily not supported"
    This functionality is temporarily disabled.

We've designed the default InvenioRDM metadata model to incorporate much of the
useful fields the digital repository community has adopted over the years. From
Subjects to Language to Location fields, there is a lot of depth to the out-of-the-box
model. We encourage you to explore it fully before you consider adding your own
fields. But adding your own fields is possible and no hacks are necessary.

Metadata extensions are defined via two configurations: the additional fields'
namespaces, a unique identifying url to prevent field collisions with other extensions,
and the extensions (fields) themselves, a name, validation schema type and
ElasticSearch storage type.

To extend the metadata model, we edit the corresponding configuration variables
in our familiar friend `invenio.cfg`. For example, we first add the new
namespace:


```python
# At the bottom
RDM_RECORDS_METADATA_NAMESPACES = {
    'dwc': {
        # A URL ensures uniqueness (it doesn't *have* to resolve)
        '@context': 'https://example.com/dwc/terms'
    }
}
```

New keys to `RDM_RECORDS_METADATA_NAMESPACES` (e.g. `'dwc'`) are shorthands for
the unique `@context` values. They are used as namespace prefixes below.

We then use the namespaces to prefix any field from that context in
`RDM_RECORDS_METADATA_EXTENSIONS`, the dict of fields:

```python
# imports at the top...
from marshmallow.fields import Bool

from invenio_records_rest.schemas.fields import SanitizedUnicode

# ...

# At the bottom after RDM_RECORDS_METADATA_NAMESPACES above
RDM_RECORDS_METADATA_EXTENSIONS = {
    'dwc:family': {
        'elasticsearch': 'keyword',
        # You could make a field required if you wanted by using required=True
        # e.g., SanitizedUnicode(required=True)
        'marshmallow': SanitizedUnicode()
    },
    'dwc:behavior': {
        'elasticsearch': 'text',
        'marshmallow': SanitizedUnicode()
    },
    'dwc:right_or_wrong': {
        'elasticsearch': 'boolean',
        'marshmallow': Bool()
    }
}
```

Each key of `RDM_RECORDS_METADATA_EXTENSIONS` is of the form: `<prefix>:<field_key>`
and each value a dict with the `'elasticsearch'` storage type and the `'marshmallow'`
storage type. As of writing, the supported Elasticsearch storage types are:
`'keyword'`, `'text'`, `'boolean'`, `'date'` and `'long'`. The supported
Marshmallow schema types are:

- `from marshmallow.fields`: `Bool`, `Integer`
- `from invenio_records_rest.schemas.fields`: `DateString`, `SanitizedUnicode`

and `marshmallow.fields.List` of the above.

Restart the server. Creating a record now looks like this:

```bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/rdm-records -d '{
    "_access": {
        "metadata_restricted": false,
        "files_restricted": false
    },
    "_owners": [1],
    "_created_by": 1,
    "access_right": "open",
    "creators": [],
    "identifiers": {
        "DOI": "10.9999/rdm.9999999"
    },
    "publication_date": "2020-08-31",
    "resource_type": {
        "type": "image",
        "subtype": "image-photo"
    },
    "titles": [{
        "title": "An Extended Record",
        "type": "Other",
        "lang": "eng"
    }],
    "descriptions": [
        {
            "description": "A story on how Julio Cesar relates to Gladiator.",
            "type": "Abstract",
            "lang": "eng"
        }
    ],
    "extensions": {
        "dwc:family": "Felidae",
        "dwc:behavior": "Plays with yarn, sleeps in cardboard box.",
        "dwc:right_or_wrong": true
    }
}'
```

You'll notice there wasn't any mention of human readable fields. We rely on the
translation system to convert the identifiers into human readable names. Make sure
to provide them to have them eventually display on the UI properly.

You are now a master of the metadata model!


## Change the permissions

Here, we show how to change the permissions required to perform actions in
the system. For the purpose of this example, we will restrict the creation of
*drafts* to super users only. To do so, we define our own
[permission policy](https://invenio-records-permissions.readthedocs.io/en/latest/usage.html#policies).

### Modify invenio.cfg

Open `invenio.cfg` in your favorite text editor (or least favorite if you
like to suffer) and add the following to the file:

```python
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.config import RDMRecordServiceConfig
from invenio_records_permissions.generators import SuperUser


class MyRecordPermissionPolicy(RDMRecordPermissionPolicy):
    can_create = [SuperUser()]


class MyBibliographicRecordServiceConfig(RDMRecordServiceConfig):
    permission_policy_cls = MyRecordPermissionPolicy


RDM_RECORDS_BIBLIOGRAPHIC_SERVICE_CONFIG = MyBibliographicRecordServiceConfig
```

Then re-start the server.

!!! info "Change the permission to publish"
    For demo purposes, *any user* can currently publish a draft. If you want to change that to only super users as well, you need to add `can_publish = [SuperUser()]` to the above policy. Don't forget to re-start the server after your changes.

When we set `RDM_RECORDS_BIBLIOGRAPHIC_SERVICE_CONFIG = MyBibliographicRecordServiceConfig`,
we are overriding the default service configuration `RDMRecordServiceConfig`provided by [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records). Many more record related features can be customized by overriding other values in the new `MyBibliographicRecordServiceConfig` class.

!!! info "Pro tip"
    You can type `can_create = []` to achieve the same effect; any empty permission list only allows super users.

That's it configuration-wise.

### Test that non super users are denied

Did the changes work? We are going to try to create a new draft.

Simply do as seen in [the previous section](./run.md#create-a-draft).
You can customize the metadata if you would like. For instance, we use
a different title.

We shorten the content for readability.

``` bash
curl -k -XPOST -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
    "access": { ... },
    "metadata": {
        "title": "A permission story",
        ...
    }
}'
```

This is what we get back:

``` json
{
    "status": 403,
    "message": "Permission denied."
}
```

As you can see, the server rejected us, because we were not a super user. Good!

### Test that super users are allowed

Let's create a user with the right permission:

``` bash
pipenv run invenio users create admin@test.ch --password=123456 --active
```

Assign them the admin role (admins have super user permission:

``` bash
pipenv run invenio roles add admin@test.ch admin
```

Generate her token where `-n` is the name of the token (your choice) and
`-u` the email of the user:


``` bash
pipenv run invenio tokens create -n permission-demo -u admin@test.ch
```

Finally, use the obtained token to perform the query:

``` bash
curl -k -XPOST -H "Authorization: Bearer <your token>" -H "Content-Type: application/json" https://127.0.0.1:5000/api/records -d '{
    ...<fill with the same json as above>...
}'
```

And it works, because we are making the API call as a user with super user access!

Revert the changes in `invenio.cfg` and restart the server to get back to where
we were.


## Add functionality

Need further customizations or additional features? If you are developing
features in an existing module, check the [Develop or edit a module section](./edit_a_module.md).
If you are creating your own extensions, check the [Extensions section](../extensions/custom.md).
