# InvenioRDM vNext


# Noteworthy changes

- A new custom base error template has been provided and configured by default in `Invenio-App-RDM` (`THEME_ERROR_TEMPLATE = "invenio_app_rdm/page_error.html"`; see [PR #3612](https://github.com/inveniosoftware/invenio-app-rdm/pull/3612)).
  This new template omits the banners from error responses (e.g. 404, 500).
  Since the banner is often the only DB query issued for requests from unauthenticated users, this can help reduce the strain on the database for spikes in traffic on unknown URL paths.
  If you have overridden this template, you might want to adapt the override.
