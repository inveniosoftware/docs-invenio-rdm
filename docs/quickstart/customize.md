# Customization

As we just saw, overriding configured values is an easy and common way of customizing your instance to your needs. Sometimes, however, you need to provide custom files too: logos, templates... We show how to perform these custom changes.

## Logo

We are going to change the logo, take an *svg* file and update your **local** static files (You can use the [invenio color logo](https://github.com/inveniosoftware/invenio-theme/blob/master/invenio_theme/static/images/invenio-color.svg)):

``` console
$ cp ./path/to/new/color/logo.svg static/images/logo.svg
```

Then, use the update command:

``` console
(your-virtualenv)$ invenio-cli update --containers
Updating static files...
```

Go to the browser [*https://localhost/*](https://localhost) or refresh the page. And voila! The logo has been changed!

**WARNING**: If you do not see it changing, check in an incognito window, the browser might have cached the logo.

## Templates

If you want to customize the look and feel of your instance, you will want to customize the templates (and CSS to come!) used.

For the templates, you can just put your new Jinja templates in the `templates/` folder and refer to them from the `invenio.cfg` file appropriately.
For example, you may have the following in your `templates/` folder:

```console
    templates/
    |__ my_front_page.html
```

In your `invenio.cfg`, you would set the appropriate configuration variable in this case:

```python
THEME_FRONTPAGE_TEMPLATE = 'my_front_page.html'
"""Frontpage template."""
```

Reload your browser to see the different template!

Most UI configuration variables are [documented here in invenio-theme](https://invenio-theme.readthedocs.io/en/latest/configuration.html).
