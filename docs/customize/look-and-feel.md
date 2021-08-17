# General look-and-feel

Adapting your instance to your needs is done by editing the `invenio.cfg` file
appropriately and/or adding files to the local folders `invenio-cli` created for
you (e.g. `app_data/`, `assets/`, `static/`, `templates/`).

The configuration file `invenio.cfg` overrides the `config.py` variables provided by
[Invenio modules](https://invenio.readthedocs.io/en/latest/general/bundles.html)
and their dependencies. Conveniently, this means that if you name your files by
the name used in the configurations for them, you won't even need to edit `invenio.cfg`!

Next, we go through modifying the principal aspects making up the look-and-feel of your instance:
the logo, the templates and the styling.
