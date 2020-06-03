# Make it your own

!!! error "Temporarily not supported"
    Due to the migration to Semantic-UI the UI customization features are not supported. They will be enabled as soon as possible. However, it is possible to customize the vocabularies, permissions, datamodel and add custom functionality. This means you can continue from the [*vocabulary customization*](#define-a-custom-controlled-vocabulary) section onwards.

You can configure and customize your InvenioRDM instance to best suit your needs.
From changing the style and look, to extending the data model and defining your
own permissions, InvenioRDM provides you with much control. And if none of this
is enough, extensions can also be created to add functionality.

Adapting your instance to your needs is done by editing the `invenio.cfg` file
appropriately and adding files to the local folders invenio-cli created for
you (e.g. `app_data/`, `assets/`, `static/`, `templates/`). The configuration file
`invenio.cfg` overrides the `config.py` variables provided by
[Invenio modules](https://invenio.readthedocs.io/en/latest/general/bundles.html)
and their dependencies. Conveniently, this means that if you name your files by
the name used in the configurations for them, you won't even need to edit `invenio.cfg`!

No worries, we go through *all* of the common customizations below.

## Change the logo

Having your instance represent your institution starts with using your
institution's logo. We are going to change InvenioRDM's default logo to your logo.

Take an *svg* file and copy it to your **local** static files.
We'll use the [invenio color logo](https://github.com/inveniosoftware/invenio-theme/raw/master/invenio_theme/static/images/invenio-color.svg) as an example:

``` bash
cp ./path/to/new/color/logo.svg static/images/logo.svg
```

Then, use the `update` command:

``` bash
invenio-cli update --no-install-js
```
``` console
# Summarized output
Collecting statics and assets...
Collect static from blueprints.
Created webpack project.
Copying project statics and assets...
Symlinking assets/...
Building assets...
Built webpack project.
```

Passing the `--no-install-js` option, skips re-installation of JS dependencies.

!!! info "Assets and statics need to be updated"
    Whenever you change files in `assets/` or `static/`, you typically want to run `invenio-cli update --no-install-js`. In case of uncertainty, just run the `update` command; it isn't destructive.

Go to the browser [*https://localhost:5000/*](https://localhost:5000) or refresh the page. And voilà! The logo has been changed!

!!! warning "That evil cache"
    If you do not see it changing, check in an incognito window; the browser might have cached the logo.

If your logo isn't an svg, you still copy it to `static/images/`, but you need to edit the `invenio.cfg` file appropriately:

```diff
- THEME_LOGO="images/logo.svg"
+ THEME_LOGO="images/my-logo.png"
```

You also need to run `update` as above and additionally restart the server:

```bash
^C
Stopping server and worker...
Server and worker stopped...
```
```bash
invenio-cli update --no-install-js
invenio-cli run
```

!!! info "Re-run when invenio.cfg changes"
    All changes to `invenio.cfg` **MUST** be accompanied by a restart like the above to be picked up. This only restarts the server; it does not destroy any data.

All other changes below follow the same pattern: add files and/or edit `invenio.cfg` and
potentially execute `update` and/or rerun the server.


## Change colors

You might also be wondering: *How do I change the colors so I can make my instance look like my institution's theme?*

We are going to change the top header section in the frontpage to apply our custom background color. Open the `assets/scss/<your instance shortname>/variables.scss` file and edit it as below:

``` scss
$navbar_background_image: unset;
$navbar_background_color: #000000; // Note this hex value is an example. Choose yours.
```

Then, run the `invenio-cli update` command as above and refresh the page! You should be able to see your top header's color changed! You can find all the available styling variables that you can change [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/scss/invenio_app_rdm/variables.scss).


## Change search results

Changing how your results are presented in the search page is also something quite common.

We are going to update the search result template so we can show more text in the result's description. Create a file called `ResultsItemTemplate.jsx` inside `assets/templates/search` folder and then edit it as below:

```js
import React from 'react';
import {Item} from 'semantic-ui-react';
import _truncate from 'lodash/truncate';

export function ResultsItemTemplate(record, index) {
  return (
    <Item key={index} href={`/records/${record.id}`}>
      <Item.Content>
        <Item.Header>{record.metadata.titles[0].title}</Item.Header>
        <Item.Description>
          {_truncate(record.metadata.descriptions[0].description, { length: 400 })}
        </Item.Description>
      </Item.Content>
    </Item>
  )
};
```

Then, run the `invenio-cli update` command as above and refresh the page! You should be able to see more text in each result's description! You can find all the available templates [here](https://github.com/inveniosoftware/invenio-app-rdm/tree/master/invenio_app_rdm/theme/assets/templates/search).


## Change the record landing page

When you click on a search result, you navigate in the details page of a specific record. This section shows you how to change the way the information is displayed in the details page.

We are going to configure our instance to use our template for displaying the information in the record's landing page. Open the `invenio.cfg` file and add the below:

```python
from invenio_rdm_records.config import RECORDS_UI_ENDPOINTS
RECORDS_UI_ENDPOINTS['recid'].update(template='my_record_landing_page.html')
```

You will note that `invenio.cfg` is really just a Python module. How convenient!

Then, we create a file `my_record_landing_page.html` inside the `templates` folder and edit it as below:

```jinja
{%- extends 'invenio_rdm_records/record_landing_page.html' %}

{%- block page_body %}
<!-- // Paste your code here -->
{%- endblock page_body %}
```

Inside the `page_body` block you can restructure the page as you want! You can check the default record landing page template [here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/theme/templates/invenio_rdm_records/record_landing_page.html).

Since we modified `invenio.cfg`, we need to re-start the server to see our changes take effect.


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

# ...

# At the bottom
# Our custom Vocabularies
RDM_RECORDS_CUSTOM_VOCABULARIES = {
    'resource_types': join(
        dirname(abspath(__file__)),
        'app_data', 'vocabularies', 'resource_types.csv')
}
```

!!! info "Other vocabularies"
    See the [Vocabulary source code](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/vocabularies/__init__.py)
    in invenio-rdm-records to know the keys for the other vocabularies.

Restart your server and your vocabulary will now be used for resource types!


## Extend the metadata model

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
curl -k -XPOST -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '{
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


## Change permissions

Here, we show how to change the permissions required to perform actions in
the system. For the purpose of this example, we will only allow super users to
create records through the REST API. To do so, we define our own permission policy.

Open the `invenio.cfg` in your favorite text editor (or least favorite if you
like to suffer) and add the following to the file:

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

and re-start the server.

When we set `RECORDS_PERMISSIONS_RECORD_POLICY = MyRecordPermissionPolicy`,
we are overriding `RECORDS_PERMISSIONS_RECORD_POLICY` provided by
[invenio-records-permissions](https://github.com/inveniosoftware/invenio-records-permissions).

!!! info "Pro tip"
    You can type `can_create = []` to achieve the same effect; any empty permission list only allows super users.

That's it configuration-wise. If we try to create a record through the API,
your instance will check if you are a super user before allowing you.

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
        "subtype": "image-photo"
    },
    "identifiers": {
        "DOI": "10.9999/rdm.0",
    },
    "creators": [
        {
            "name": "Marcus Junius Brutus",
            "type": "Personal",
            "given_name": "Marcus",
            "family_name": "Brutus",
            "identifiers": {
                "Orcid": "9999-9999-9999-9990"
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
            "title": "A permission story",
            "type": "Other",
            "lang": "eng"
        }
    ],
    "descriptions": [
        {
            "description": "A story about how permissions work.",
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

Let's create a user with the right permission, generate her token and use the API
with it.

``` bash
pipenv run invenio users create admin@test.ch --password=123456 --active
```

``` bash
pipenv run invenio roles add admin@test.ch admin
```

Login through the browser as `admin@test.ch` with password `123456`. Then
in the dropdown menu of the username (top-right), select `Applications`. Then
click on `New token`, name your token and click `Create`. Copy this token (we
will refer to it as `<your token>`) and put it in the API call as such:

Alternatively, you can get a token using the invenio command, where `-n` is
the name of the token (your choice) and `-u` the email of the user created
right before.

``` bash
 pipenv run invenio tokens create -n permission-demo -u admin@test.ch
 ```

Then use the obtained token to perform the query:

``` bash
curl -k -XPOST -H "Authorization:Bearer <your token>" -H "Content-Type: application/json" https://localhost:5000/api/records/ -d '{
    ...<fill with the above>...
}'
```

And it works! That's because InvenioRDM creates an `admin` role with super user
access permissions when initially setting up the database. Above, we set
`admin@test.ch` to be an admin, so that user can create records.

Revert the changes in `invenio.cfg` and restart the server to get back to where
we were.


## Add functionality

Need further customizations or additional features? Have you thought of
creating your own extensions?

How to make an extension and add it to your InvenioRDM instance is explained in
the [Extensions section](../extensions/custom.md).
