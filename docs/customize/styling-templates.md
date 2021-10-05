# Change a page (template)

When you click on a search result, you navigate to the details page of a specific record, often called the record landing page. This section shows you how to change this page. The same approach is used to change any other Jinja-template-backed page.

For now, InvenioRDM supports overriding the pre-existing templates by placing customized ones with same filepath in the `templates/` folder.

### Change the landing page

To override the record landing page, add the following folders and file in your `templates/` folder: `semantic-ui/invenio_app_rdm/records/detail.html`. Notice how this mirrors the path to `detail.html` in invenio-app-rdm from the [records_ui](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/) directory:

**Your file hierarchy**

```
templates
└── semantic-ui
    └── invenio_app_rdm
        └── records
            └── detail.html
```

**Invenio-app-rdm's file hierarchy from records_ui/**

```
templates
└── semantic-ui
    └── invenio_app_rdm
        └── records
            └── detail.html
```


Edit this file as you see fit:

```jinja
{%- extends config.BASE_TEMPLATE %}

{%- block head_title %}
  <title>My Customized title!</title>
{%- endblock head_title %}
```

You can check the default record landing page template [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/invenio_app_rdm/records/detail.html) for inspiration. By creating a file with the same path as that one relative to the `templates/` folder, our file is chosen over the default one.


### Change other pages

The same pattern applies for any page. Copy the filepath relative to `templates/` in [invenio-app-rdm](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/) into your instance's `templates/` folder. This way, your file is chosen rather than the default one. For example, having `templates/semantic-ui/invenio_app_rdm/records/export.html` in your instance, will make that template be used for generating the export page html.

This also applies to wherever a `templates/` is found e.g. the footer can be customized by copying and editing `footer.html` from
[invenio-app-rdm/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm](https://github.com/inveniosoftware/invenio-app-rdm/tree/master/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm): you would have `templates/semantic-ui/invenio_app_rdm/footer.html` in your file hierarchy.
