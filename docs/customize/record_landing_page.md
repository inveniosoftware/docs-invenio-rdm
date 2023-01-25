# Record landing page

InvenioRDM supports customization of some of the sections of the record's landing page.

### Citation styles

InvenioRDM supports citations styles defined in the [CSL 1.0.1 specifications](https://docs.citationstyles.org/en/v1.0.1/specification.html). You can find the list of all possible citation styles [here](https://github.com/citation-style-language/styles/tree/v1.0.1).

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

### Download all files button

*Introduced in InvenioRDM v11*

!!! warning "Blocking connection and large files"
     In contrast to other file-serving endpoints, this functionality does not offload the response to nginx, which means that for very large files and slower client connections these might become long-running blocking requests. You can mitigate these issues either via rate-limiting or setting up dedicated resources for serving this type of requests.

To enable/disable the UI button and backend functionality for being able to download all of a record's files as a single ZIP file, you can set in your `invenio.cfg` the following config:

```python
RDM_ARCHIVE_DOWNLOAD_ENABLED = True
```
