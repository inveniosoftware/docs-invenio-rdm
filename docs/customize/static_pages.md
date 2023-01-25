# Static pages

*Introduced in InvenioRDM v11*

InvenioRDM supports an easy "out-of-the-box" way of creating static pages, basically web pages for which the HTML content is stored in the database
and you can, in the future versions of InvenioRDM, change it using the administration panel.

## Define pages

To add the new static pages, create a file named `pages.yaml` in the `app_data` folder:

```
app_data/
└── pages.yaml
```

Then, inside the file, define the URL, the title, the description and the HTML template of each static page:

```yaml
# list of pages:
- url: /help/search
  title: Search guide
  description: Search guide
  template: search_guide.html
```

InvenioRDM will look for the content of each static page in the `template` HTML file, located in a new sub-folder named `pages`:

```
app_data/
└── pages
    └──search_guide.html
```

The HTML file content is what will be imported in the database and rendered to the user when navigating to the page's URL.

## Load pages

To load the new static page to your instance, you have 2 options:

1. Run the instance setup command `invenio-cli services setup`: the command will find the pages defined as above and load them. **Warning: this command will delete all your data!**

2. In a previously created instance folder, run:

```bash
pipenv run invenio rdm pages create
```

You can use the `--force` option to wipe out all previously created static pages and load them again.
