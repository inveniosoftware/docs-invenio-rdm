# Subjects

Subjects are another special type of vocabulary. By default InvenioRDM comes
with the [OECD FOS](http://oecd.org/science/inno/38235147.pdf) list of terms.
However, you can add your custom ones like such:

**vocabularies.yaml**

```yaml
subjects:
  pid-type: sub
  schemes:
    - id: MYSCHEME
      name: My subject scheme
      uri: "https://example.com/my/scheme"
      data-file: vocabularies/subjects_my_scheme.yaml
```

**vocabularies/subjects_my_scheme.yaml**

```yaml
- id: "https://example.com/my/scheme/1"
  scheme: MYSCHEME
  subject: "My term 1"
- id: "https://example.com/my/scheme/2"
  scheme: MYSCHEME
  subject: "My term 2"
```

Extensions can also provide subjects. For instance, you can also add
[MeSH](https://www.ncbi.nlm.nih.gov/mesh/) terms via the [invenio-subjects-mesh](https://github.com/galterlibrary/invenio-subjects-mesh)
package. This package is provided by Northwestern University, and we hope that more such packages provided by members of the community will become common.

In order to install that extension:

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
