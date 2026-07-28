# File previewers

InvenioRDM uses the Invenio-Previewer module to provide frontend components that render previews for common file types on the record landing page.

Supported preview types (examples):

- CSV (papaparse / d3)
- Images (PNG, JPEG, GIF), including IIIF
- XML, JSON, GeoJSON
- Markdown
- PDF
- Audio and video
- Jupyter Notebooks
- ZIP archives
- Plain text (txt)
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
    # "web_archive",    # web archive previewer (optional)
]
```

Notes:
- Previewers match on file extension and sometimes file content.
- Order matters: the system selects the first previewer that claims compatibility. Put specific previewers (e.g. image previewer) before generic ones (e.g. text) to avoid incorrect matches.

## Custom previewers

To create and register a custom previewer, follow the Invenio-Previewer documentation for the previewer API and registration instructions:

- https://invenio-previewer.readthedocs.io/en/latest/usage.html#custom-previewer

If you implement a previewer, add its identifier to PREVIEWER_PREVIEWERS and ensure its matching logic is precise to avoid conflicts with existing previewers.
