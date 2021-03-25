# Styling

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
invenio-cli assets build
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

This command makes sure files you have in `static/`, `assets/`, `templates/` and so on are placed in the right location with other similar files for the application. The files are by default symlinked to ensure future modifications to those files translate directly. No need to run `invenio-cli assets build` again for them.

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

Open the `assets/less/site/globals/site.variables` file and edit it as below:

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


