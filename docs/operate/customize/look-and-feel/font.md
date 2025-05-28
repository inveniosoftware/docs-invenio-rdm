# Change the font

You might also be wondering: *How do I change the font so I can make my instance adopt my institution's theme?*
There are different ways to add fonts to your InvenioRDM instance. You can either include Google Fonts by adding a link or add fonts locally. In this guide, we'll cover the steps to add fonts locally.

## Step-by-step

### 1. Add the font files

In your instance's `assets/less/site/fonts` directory, add the font files you want to use. For example, if you want to use the "Figtree" and "Open Sans" fonts, you would add the following files:

```bash
./assets/less/site/fonts/Figtree.woff2
./assets/less/site/fonts/OpenSans.ttf
```

### 2. Define the font faces

In `assets/less/site/globals/site.overrides` add the following code to define the font faces:

```less
@font-face {
  font-family: "Figtree";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("../fonts/Figtree-Regular.woff2") format("woff2");
}

@font-face {
  font-family: "Open Sans";
  font-optical-sizing: auto;
  font-style: normal;
  font-weight: 400;
  src: url("../fonts/OpenSans.ttf") format("truetype");
}

```

### 3. Use the fonts in your site

To use the fonts in your site, you can use the following in your `assets/less/site/globals/site.variables`:

``` less
/* Fonts */
@fontName: "Figtree", Arial, Helvetica, sans-serif;
@pageFont: "Open Sans", Arial, Helvetica, sans-serif;
@headerFont: @fontName;
```

### 4. Build the assets

After making the changes, build the assets by running the following command:

```bash
invenio-cli assets build -d
```

> **Note**: When you add the fonts while using `invenio-cli assets watch`, you need to cancel the process, build assets and start the watch again to avoid any issues.

After following these steps, your InvenioRDM instance should now use the specified fonts, reflecting your institution's theme.
