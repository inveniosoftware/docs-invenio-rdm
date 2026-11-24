# File previewers

InvenioRDM uses the Invenio-Previewer module to provide frontend components that render previews for common file types on the record landing page.

Supported preview types:

- CSV
- Images (PNG, JPEG, GIF), including IIIF
- XML, JSON, GeoJSON
- Markdown
- PDF
- Audio and video
- Jupyter Notebooks
- ZIP archives
- Plain text
- Web archives

## Enabling previewers

Previewers are configured via the PREVIEWER_PREVIEWERS setting. Add the previewer identifiers you want in your configuration (e.g. config.py):

```python
PREVIEWER_PREVIEWERS = [
    "csv_papaparsejs",  # CSV
    # "iiif_simple",    # IIIF for images (optional)
    "simple_image",     # images
    "json_prismjs",     # JSON / GeoJSON
    "xml_prismjs",      # XML
    "mistune",          # Markdown
    "pdfjs",            # PDF
    "video_videojs",    # Video
    "audio_videojs",    # Audio
    "ipynb",            # Jupyter notebooks
    "zip",              # ZIP archives
    "txt",              # plain text
    # "web_archive",    # web archive previewer (optional, see below)
]
```

Notes:
- Previewers match on file extension and sometimes file content.
- Order matters: the system selects the first previewer that claims compatibility. Put specific previewers (e.g. image previewer) before generic ones (e.g. text) to avoid incorrect matches.

## Web archive previewer

The web archive previewer displays WACZ, WARC, HAR, CDX and CDXJ files using an embedded [ReplayWeb.page](https://replayweb.page/) viewer. It is disabled by default.

!!! warning "Serve the web archive previewer from a separate domain"

    A web archive is a recording of real websites, including their HTML and JavaScript. To replay it faithfully, the previewer runs that recorded JavaScript in the browser. If the previewer is served from the same domain as your InvenioRDM instance, that code runs with the same permissions as InvenioRDM itself: it could, for example, act on behalf of the logged-in user. In practice, anyone who can upload a web archive could run their own scripts in other visitors' sessions (a form of cross-site scripting, XSS).

    The previewer ships with Content Security Policy (CSP) rules that reduce this risk, but they cannot remove it entirely, because running the archived scripts is exactly what the previewer is designed to do.

    For this reason, **only enable the web archive previewer if you serve it from a dedicated domain or sub-domain** that does not share cookies or sessions with your main site (e.g. `previewer.example-usercontent.org` for an instance running on `repository.example.org`). This is a common practice for platforms that display user-provided content. If you cannot set up a separate domain, we recommend keeping this previewer disabled.

## Custom previewers

To create and register a custom previewer, follow the Invenio-Previewer documentation for the previewer API and registration instructions:

- https://invenio-previewer.readthedocs.io/en/latest/usage.html#custom-previewer

If you implement a previewer, add its identifier to PREVIEWER_PREVIEWERS and ensure its matching logic is precise to avoid conflicts with existing previewers.
