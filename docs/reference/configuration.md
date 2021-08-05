# Configuration reference

### ``RDM_CITATION_STYLES``

InvenioRDM has a configuration option called ``RDM_CITATION_STYLES`` which controls which citation styles will show up on the landing page:

``` python
RDM_CITATION_STYLES = [
     ('chicago-annotated-bibliography', _('Chicago')),
     ('ieee', _('IEEE')),
     ('science', _('Science')),
     ('apa', _('APA')),
     ('cell', _('Cell')),
]
```

### ``RDM_DEFAULT_CITATION_STYLE``

This option called ``RDM_DEFAULT_CITATION_STYLE`` controls which citation style will be the default one showing up on the landing page:

```
RDM_DEFAULT_CITATION_STYLE = 'chicago-annotated-bibliography'
```

Note that the default citation style must be one of the available configured above.
