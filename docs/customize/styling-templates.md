# Change the record landing page

When you click on a search result, you navigate to the details page of a specific record, often called the record landing page. This section shows you how to change this page.

For now, we support overriding the pre-existing templates by placing customized ones with same filepath in the `templates/` folder.

To override the record landing page, add the following folders and file in your `templates/` folder: `semantic-ui/invenio_app_rdm/records/detail.html`. Edit this file as you see fit:


```jinja
{%- extends config.BASE_TEMPLATE %}

{%- block head_title %}
  <title>My Customized title!</title>
{%- endblock head_title %}
```

You can check the default record landing page template [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/invenio_app_rdm/records/detail.html) for inspiration. By creating a file with the same path as that one relative to the `templates/` folder, our file is chosen over the default one.


### Change other pages

The same pattern applies for any page. Copy the filepath relative to `templates/semantic-ui/` in [invenio-app-rdm](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/) into your instance's `templates/` folder. This way your file is chosen rather than the default one. For example, having `templates/invenio_app_rdm/records/export.html` in your instance, will make that template be used for generating the export page html.


