# How to add JavaScript files

This documentation is targeted to developers who want to add new JavaScript files in InvenioRDM.

In InvenioRDM, JavaScript files are part of bundles, which are basically multiple JavaScript files grouped together.
Bundles are discovered in all InvenioRDM modules and built using [webpack](https://webpack.js.org/) to
optimize them and make them production-ready.

## Prerequisite

To add new JavaScript files, you will need to create a module or use the `site` folder of your InvenioRDM instance.
The how-to [Creating custom code and views](custom_code.md) guides you on creating a `site` folder and on adding JavaScript files for specific web pages.

## Global JavaScript

The following guide assumes that you have read the previous section and how-to guide, as it references to it.

You might need to add some JavaScript code globally on your website (e.g. web analytics), and not only just executed when visiting a specific web page. The steps are similar to the ones needed to add a JavaScript file for a specific view:

1. Create a new JavaScript file with your code.
2. Add the file to the `webpack.py` to register the new entry in the bundle and give it a name `my-site-global`.

The difference now is that instead of adding the new bundle in a specific Jinja template (e.g. `support.html`), you will need to add it to the global JavaScript files block added in the base Jinja template footer, defined in <a href="https://github.com/inveniosoftware/invenio-theme/blob/master/invenio_theme/templates/semantic-ui/invenio_theme/page.html" target="_blank">`invenio-theme/page.html`</a>.

Create a new template `page.html` file with its path matching the original Invenio-Theme module's file:

```
├── site
│   ├── my_site
│   │   ├── templates/semantic-ui/invenio_theme/page.html
```

Then, override the `javascript` block, calling `super` to make sure other global JavaScript files are included:

```jinja
...

{% block javascript %}
    {{ super() }}
    {{ webpack['my-site-support.js'] }}
{% endblock %}
```

!!! note

    You might have already defined your own `page.html` to customize the global look and feel of your theme:
    change that file instead of creating a new one.

    This guide assumes that you did not change the variable `BASE_TEMPLATE`: if that's the case, you will have
    to re-define the template file set in that variable.
