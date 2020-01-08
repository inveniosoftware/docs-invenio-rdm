# Customization

As we just saw, overriding configured values is an easy and common way of customizing your instance to your needs. Sometimes, however, you need to provide custom files too: logos, templates... We show how to perform these custom changes.

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
