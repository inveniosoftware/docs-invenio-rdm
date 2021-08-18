# Styling

Adapting your instance to your needs is done by editing the `invenio.cfg` file
appropriately and adding files to the local folders invenio-cli created for
you (e.g. `app_data/`, `assets/`, `static/`, `templates/`). The configuration file
`invenio.cfg` overrides the `config.py` variables provided by
[Invenio modules](https://invenio.readthedocs.io/en/latest/documentation/bundles/index.html)
and their dependencies. Conveniently, this means that if you name your files by
the name used in the configurations for them, you won't even need to edit `invenio.cfg`!

We go through common customizations and show you the workflow below.
