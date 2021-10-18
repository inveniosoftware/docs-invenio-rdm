# Change the theme

You might also be wondering: *How do I change the colors so I can make my instance adopt my institution's theme?*

The theme comprises the header, footer and main color(s). We are going to modify them. It's a good example of the workflow for when `assets/` files change.

Open the `assets/less/site/globals/site.overrides` file and edit it as below:

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

You can override any styling variables in your `site.overrides` file. The available styling variables are found in the `variables.less` or `.variables` files of the various invenio modules installed. The ones above are originally defined [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/less/invenio_app_rdm/variables.less). The `invenio-theme` module defines a large number of them [here](https://github.com/inveniosoftware/invenio-theme/tree/master/invenio_theme/assets/semantic-ui/less/invenio_theme/theme).

However, you may notice further changes to the `site.overrides` file are not picked up unless `invenio-cli assets build` is run again each time even though we symlinked these files! That's because `.less` files (and javascript files below) always need to be transformed into their final form first. `invenio-cli assets build` does that. There is a way to get the same workflow as `static/` files, without having to re-run that command over and over: run `invenio-cli assets watch`. It watches for changes to assets and rebuilds them automatically.

The workflow for `assets/` files is then:

- Start `invenio-cli assets watch` in a terminal (you will need a different terminal for the other commands).
- If you add a new file, run `invenio-cli assets build -d`.
- If you modify `invenio.cfg`, re-run `invenio-cli run`.
- If you modify a previously symlinked file, you now don't need to do anything.
