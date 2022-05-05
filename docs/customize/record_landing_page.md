# Record landing page

InvenioRDM supports customization of some of the sections of the record's landing page.

### Citation styles

InvenioRDM supports citations styles defined in the [CSL 1.0.1 specifications](https://docs.citationstyles.org/en/1.0.1/specification.html). You can find the list of all possible citation styles [here](https://github.com/citation-style-language/styles/blob/6152ccea8b7d7a472910d36524d1bf3557a83bfc/renamed-styles.json).

In the record landing page, you can display a subset of the available styles. In your `invenio.cfg` change:

```
RDM_CITATION_STYLES = [
     ('chicago-annotated-bibliography', _('Chicago')),
     ('ieee', _('IEEE')),
     ('science', _('Science')),
     ('apa', _('APA')),
     ('cell', _('Cell')),
]
```

By changing the list above, these styles will be visible in the record landing page and the user can click on them to change citation style.

You can change the default citation style used when loading the record landing page by setting:

```
RDM_CITATION_STYLES_DEFAULT = 'chicago-annotated-bibliography'
```
