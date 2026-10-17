# File previewers

InvenioRDM uses the [Invenio-Previewer module](https://github.com/inveniosoftware/invenio-previewer) to provide frontend components that render previews for common file types on the record landing page.

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

Previewers are configured via the `PREVIEWER_PREFERENCE` setting. Add the previewer identifiers you want in your configuration:

```python
PREVIEWER_PREFERENCE = [
    "csv_papaparsejs",  # CSV
    "pdfjs",            # PDF
    # "iiif_simple",    # IIIF for images (optional)
    "simple_image",     # images
    "json_prismjs",     # JSON / GeoJSON
    "xml_prismjs",      # XML
    "mistune",          # Markdown
    "video_videojs",    # Video
    "audio_videojs",    # Audio
    "ipynb",            # Jupyter notebooks
    # "zip",            # basic ZIP archive previewer
    "previewable_zip",  # advanced ZIP archive previewer
    "txt",              # plain text
    # "web_archive",    # web archive previewer (optional)
]
```

Notes:
- Previewers match on file extension and sometimes file content.
- Order matters: the system selects the first previewer that claims compatibility. Put specific previewers (e.g. image previewer) before generic ones (e.g. text) to avoid incorrect matches.

## Custom previewers

To create and register a custom previewer, follow the Invenio-Previewer documentation for the previewer API and registration instructions at [https://invenio-previewer.readthedocs.io/en/latest/usage.html#custom-previewer](https://invenio-previewer.readthedocs.io/en/latest/usage.html#custom-previewer).

If you implement a previewer, add its identifier to `PREVIEWER_PREFERENCE` and ensure its matching logic is precise to avoid conflicts with existing previewers.
