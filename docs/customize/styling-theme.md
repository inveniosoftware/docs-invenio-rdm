# Change the theme

You might also be wondering: *How do I change the colors so I can make my instance adopt my institution's theme?*

The theme comprises the header, footer and main color(s). We are going to modify them. It's a good example of the workflow for when `assets/` files change.

Open the `assets/less/site/globals/site.variables` file and edit it to have the following:

``` less
@brandColor: /* your brand color here */ ;
@navbarBackgroundImage: url("/static/images/your_image.png");
@navbarBackgroundColor: @brandColor;
@footerLightColor: @brandColor;
@footerDarkColor: /* a shade of your brandColor */;
```

!!! info Important:

Full list of available Semantic UI [variables](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/master/themes/default/globals/site.variables)

Full list of Invenio App RDM [variables](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/less/invenio_app_rdm/theme/globals/site.variables)


Then, run the `invenio-cli assets build -d` command as above and refresh the page! You should be able to see your theme color(s)!

You can override any styling variables in your `site.variables` file. The available styling variables are found in the `variables.less` or `.variables` files of the various invenio modules installed. The ones above are originally defined [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/less/invenio_app_rdm/variables.less). The `invenio-theme` module defines a large number of them [here](https://github.com/inveniosoftware/invenio-theme/tree/master/invenio_theme/assets/semantic-ui/less/invenio_theme/theme).

However, you may notice further changes to the `site.variables` file are not picked up unless `invenio-cli assets build` is run again each time even though we symlinked these files! That's because `.less` files (and javascript files below) always need to be transformed into their final form first. `invenio-cli assets build` does that. There is a way to get the same workflow as `static/` files, without having to re-run that command over and over: run `invenio-cli assets watch`. It watches for changes to assets and rebuilds them automatically.

The workflow for `assets/` files is then:

- Start `invenio-cli assets watch` in a terminal (you will need a different terminal for the other commands).
- If you add a new file, run `invenio-cli assets build -d`.
- If you modify `invenio.cfg`, re-run `invenio-cli run`.
- If you modify a previously symlinked file, you now don't need to do anything.
