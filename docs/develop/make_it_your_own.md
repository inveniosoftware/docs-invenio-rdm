# Make it your own

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

We go through common customizations and show you the workflow below.

## Change the logo

Having your instance represent your institution starts with using your
institution's logo. We are going to change InvenioRDM's default logo to your logo.

Take an *svg* file and copy it to your **local** static files.
We'll use the [invenio color logo](https://github.com/inveniosoftware/invenio-theme/raw/master/invenio_theme/static/images/invenio-color.svg) as an example:

``` bash
cp ./path/to/new/color/logo.svg static/images/invenio-rdm.svg
```

Then, use the `assets build` command:

``` bash
invenio-cli assets build --development
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

This command makes sure files you have in `static/`, `assets/`, `templates/` and so on are placed in the right location with other similar files for the application.
The `--development` (or `-d` for short) does so by symlinking the files, while the `--production` (or `-p` for short) copies the files over. Symlinking makes future
modifications to those files translate directly. No need to run `invenio-cli assets build` again for them.

In the browser, go to [https://127.0.0.1:5000/](https://127.0.0.1:5000) or refresh the page. And voilà! The logo has changed!

!!! warning "That evil cache"
    If you do not see it changing, check in an incognito window; the browser might have cached the logo.

If your logo isn't an svg, you still copy it to `static/images/`, but you need to edit the `invenio.cfg` file appropriately:

```diff
- THEME_LOGO="images/logo.svg"
+ THEME_LOGO="images/my-logo.png"
```

Then, run `assets build` as above and additionally restart the server:

```bash
^C
Stopping server and worker...
Server and worker stopped...
```
```bash
invenio-cli assets build -d
invenio-cli run
```

!!! info "Re-run when invenio.cfg changes"
    All changes to `invenio.cfg` **MUST** be accompanied by a restart like the above to be picked up. This only restarts the server; it does not destroy any data.

This workflow stands for all `static/` files:

- if you add a new file, run `invenio-cli assets build -d`
- if you modify `invenio.cfg`, re-run `invenio-cli run` (because `invenio.cfg` has been symlinked above, you don't need to run `assets build`)
- if you modify a previously symlinked file, you don't need to do anything


## Change the theme

You might also be wondering: *How do I change the colors so I can make my instance adopt my institution's theme?*

The theme comprises the header, footer and main color(s). We are going to modify them. It's a good example of the workflow for when `assets/` files change.

Open the `assets/less/variables.less` file and edit it as below:

``` less
@brandColor: /* your brand color here */ ;

@navbar_background_image: unset;
@navbar_background_color: @brandColor;
@footerLightColor: @brandColor;
@footerDarkColor: /* a shade of your brandColor */;
```

!!! info "Less configuration in the future"

    We plan on requiring even less variable overrides in the future to change the theme.
    `@navbar_background_color` could be preset to the brand color and so on for example.

Then, run the `invenio-cli assets build -d` command as above and refresh the page! You should be able to see your theme color(s)!

You can override any styling variables in your `variables.less` file. The available styling variables are found in the `variables.less` or `.variables` files of the various invenio modules installed. The ones above are originally defined [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/less/invenio_app_rdm/variables.less). The `invenio-theme` module defines a large number of them [here](https://github.com/inveniosoftware/invenio-theme/tree/master/invenio_theme/assets/semantic-ui/less/invenio_theme/theme).

However, you may notice further changes to the `variables.less` file are not picked up unless `invenio-cli assets build` is run again each time even though we symlinked these files! That's because `.less` files (and javascript files below) always need to be transformed into their final form first. `invenio-cli assets build` does that. There is a way to get the same workflow as `static/` files, without having to re-run that command over and over: run `invenio-cli assets watch`. It watches for changes to assets and rebuilds them automatically.

The workflow for `assets/` files is then:

- start `invenio-cli assets watch` in a terminal (you will need a different terminal for the other commands)
- if you add a new file, run `invenio-cli assets build -d`
- if you modify `invenio.cfg`, re-run `invenio-cli run`
- if you modify a previously symlinked file, you now don't need to do anything


## Change the record landing page

When you click on a search result, you navigate to the details page of a specific record, often called the record landing page. This section shows you how to change this page.

For now, we support overriding the pre-existing templates by placing customized ones with same filepath in the `templates/` folder.

To override the record landing page, add the following folders and file in your `templates/` folder: `invenio_app_rdm/records/detail.html`. Edit this file as you see fit:


```jinja
{%- extends config.BASE_TEMPLATE %}

{%- block head_title %}
  <title>My Customized title!</title>
{%- endblock head_title %}
```

You can check the default record landing page template [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/invenio_app_rdm/records/detail.html) for inspiration. By creating a file with the same path as that one relative to the `templates/` folder, our file is chosen over the default one.


### Change other pages

The same pattern applies for any page. Copy the filepath relative to `templates/semantic-ui/` in [invenio-app-rdm](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/) into your instance's `templates/` folder. This way your file is chosen rather than the default one. For example, having `templates/invenio_app_rdm/records/export.html` in your instance, will make that template be used for generating the export page html.


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
we are overriding the default service configuration `BibliographicRecordServiceConfig`provided by [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records). Many more record related features can be customized by overriding other values in the new `MyBibliographicRecordServiceConfig` class.

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
