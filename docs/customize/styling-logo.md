# Change the logo

Having your instance represent your institution starts with using your institution's logo. We are going to change InvenioRDM's default logo to your logo.
There are two ways to achieve this goal: first you can just replace the current logo file by your own, alternatively, you can modify the configuration to use a different file.

## Replace the current logo file

The default configuration uses, as the website logo, the file `static/images/invenio-rdm.svg` of your local installation. If you wish to change the logo of the page, you must replace that file by your own logo. Ensure that your logo file has the same file extension (*svg*).

``` bash
cp static/images/logo-invenio-white.svg static/images/invenio-rdm.svg
```

After replacing the logo file, you need to use the `assets build` command:

``` bash
invenio-cli assets build
```

This command makes sure files you have in `static/`, `assets/`, `templates/` and so on are placed in the right location with other similar files for the application. 

Once the `assets build` command has finished running, you can reload your InvenioRDM website (or access it for the first time) to check that the logo has changed to your custom log.

!!! warning "That evil cache"
    If you do not see it changing, check in an incognito window; the browser might have cached the logo.

## Change the configuration

If your wish to use a logo file with a different name (for example, because the logo file isn't an svg) you will need first to copy your logo in the folder `static/images/` of your local installation and then edit your `invenio.cfg` file appropriately:

```diff
- THEME_LOGO = 'images/invenio-rdm.svg'
+ THEME_LOGO = 'images/your-logo-filename.extension'
```

For the new file to be taken into account you must, as explained before, run the `assets build` command.
``` bash
invenio-cli assets build
```

Aditionally, once you modify the configuration of the application, you have to stop and restart the server. For stopping the server you just have to go to the terminal in which your server is running and press `Ctrl + C`. No data will be lost by this action. After stopping the server, you just need to run it again.
```bash
invenio-cli run
```
After this steps, you can reload your InvenioRDM site to check that the logo has changed.

