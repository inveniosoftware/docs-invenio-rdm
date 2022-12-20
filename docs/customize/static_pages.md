# Static pages

InvenioRDM supports an easy "out-of-the-box" way of creating static pages.

Static pages are loaded through the application data folder. A file named `pages.yaml` must be created and added in the root of the `app_data` folder.

```
app_data/
└── pages.yaml
```

The content of the file is as follows:

```yaml
#list of pages:
- url: /help/search
  title: Search guide
  description: Search guide
  template: search_guide.html
```

The templates used for each page must be provided in the application data folder as well, but in the `pages` folder.

```
app_data/
└── pages
    └──search_guide.html
```

The templates contain the content that will be displayed in the static pages.

Static pages are loaded during the setup (`invenio-cli services setup`). But can also be loaded any time by using the following command.

```bash
pipenv run invenio rdm-records pages create
```

A `force` option is avalaible to wipe out all previous static pages and load them again.
