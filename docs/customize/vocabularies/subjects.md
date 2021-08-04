# Subjects (MeSH)

Subjects are another special type of vocabulary. By default InvenioRDM comes
with the [OECD FOS](http://oecd.org/science/inno/38235147.pdf) list of terms.
However, you can add others like [MeSH](https://www.ncbi.nlm.nih.gov/mesh/).

In order to do so, you simply need to install [invenio-subjects-mesh](https://github.com/galterlibrary/invenio-subjects-mesh).

```
cd /path/to/your/instance
pipenv install invenio-subjects-mesh
```

You should see the dependency being added to the `Pipfile`.

Then you need to run the fixtures command and start your instance (if not running already).

```
invenio rdm-records fixtures
invenio-cli run
```