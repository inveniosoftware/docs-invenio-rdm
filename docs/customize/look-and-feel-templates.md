# Change the templates

Jinja templates are used to define the content of each page. For example, when you click on a search result,
you navigate to the details page of a specific record, often called the record landing page. This section shows you how to change
this page and any other template-based page in InvenioRDM.

### Override templates via the `templates/` folder

For now, we support overriding the pre-existing templates by placing customized ones with same filepaths in the `templates/` folder of the instance.

To override the record landing page, you would add the following folders and file in your `templates/` folder:
`semantic-ui/invenio_app_rdm/records/detail.html`. Then edit this file as you see fit:

```jinja
{%- extends config.BASE_TEMPLATE %}

{%- block head_title %}
  <title>My Customized title!</title>
{%- endblock head_title %}
```

You can look at the default record landing page template [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/records_ui/templates/semantic-ui/invenio_app_rdm/records/detail.html) for inspiration.

Refresh your browser and you will see your modification take effect. By creating a file with the same path as the default one, but relative to the `templates/` folder, our file was chosen over the default one.

### Change other pages

The same pattern applies for any page. If the default file is located in `/invenio_app_rdm/records_ui/templates/semantic-ui/<path>/<to>/<file>.html`,
copy it into your instance as `templates/semantic-ui/<path>/<to>/<file>.html`. This way your file is chosen rather than the default one.
