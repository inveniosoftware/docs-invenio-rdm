# Change the theme

You might also be wondering: *How do I change the colors so I can make my instance adopt my institution's theme?*

The theme or branding comprises the colors used for the header, footer and accent. We are going to modify them. It's a good example of the workflow for when `assets/` files change.

## Step-by-step

**Step 1** - Edit the appropriate `.variables` or `.overrides` files.

The `assets/less/site/globals/site.variables` is where you can override site wide less variables. Edit it as you see fit:

``` less
/* Override @primaryColor to override the site-wide accents. */
@primaryColor: /* your brand color */;

/* Header */
/* Override @navbarBackgroundImage to override the header background. */
@navbarBackgroundImage: linear-gradient(12deg, /* your color */, /* your color */ 15%, rgba(251, 130, 115, 0.69));
/* It can also literally be an image. */
@navbarBackgroundImage: url("/static/images/your_image.png");
/* For a flat color use @navbarBackgroundColor instead. */
@navbarBackgroundColor: /* your color */;

/* Footer */
@footerLightColor: @brandColor;
@footerDarkColor: /* a shade of your brandColor */;
```

You can override any styling variable in your `site.variables` file. The available styling variables are typically found in the `.variables` files of the various Invenio modules installed (see note below).
For instance, To change the orange search button color, in your instance create `assets/less/site/elements/button.variables` file (notice the use of the elements folder instead of the globals one) and add the following line to it:

```less
@searchButtonColor: /* your desired color */;
```

!!! info "List of variables that can be overridden"

    Full list of available Semantic UI [variables](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/master/themes/default/globals/site.variables).

    Full list of Invenio App RDM [variables](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/less/invenio_app_rdm/theme/globals/site.variables).

To override InvenioRDM's or Semantic-UI's rules, do the same as above but for the selected `.overrides` file. For instance, you could edit the `site.overrides` to change the color of links:

``` less
/* Override a to override the color of links site-wide. */
a {
    color: /* link color */;
}
```

!!! info "List of overrides"

    Full list of available Semantic UI [overrides](https://github.com/Semantic-Org/Semantic-UI/tree/master/src/themes/default).

    Full list of Invenio theme [overrides](https://github.com/inveniosoftware/invenio-theme/tree/master/invenio_theme/assets/semantic-ui/less/invenio_theme/theme).


To know more about the philosophy behind theming see the [Theming section](../../develop/topics/theming.md).

**Step 2** - Run the `invenio-cli assets build` command.

Wait a minute! These files were symlinked. You may wonder why we need to run `invenio-cli assets build`.
You will notice that any changes to the `site.variables` file are not picked up, unless `invenio-cli assets build` is run again each time. And this is the case even though we symlinked these files!

That's because `.less` files (and React files) always need to be transformed into their final form first (`.css` files). `invenio-cli assets build` does that *in addition* to placing the files/links in the right places. Thankfully, there is a way to get the same workflow as `static/` files, without having to re-run `invenio-cli assets build` over and over.

## Automatic re-build

That way is to run `invenio-cli assets watch` in a separate terminal. This command watches for changes to assets and rebuilds them automatically. It runs indefinitely until you cancel it via `<Ctrl+C>`.

It needs to "know" the assets already however. This means you still need to run `invenio-cli assets build` if you have added a new file to `assets/`.

## Custom assets files workflow

The workflow for `assets/` files is then:

- Start `invenio-cli assets watch` in a terminal (you will need a different terminal for the other commands).
- If you add a new file, then run `invenio-cli assets build`.
- If you modify a previously symlinked file, you now don't need to do anything.
