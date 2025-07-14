# Sitemaps

_Introduced in v13_

[Sitemaps](https://sitemaps.org/) are a longstanding way to layout the pages of a website in a format that a search engine (or other such crawler) can efficiently parse and, in turn, serve as search results. They make your instance's content directly available to search engines even if no other pages on the web have linked to them yet and can even enhance your standing in a search engine's offerings.

In InvenioRDM, sitemaps are automatically generated and updated. This covers both sitemap indices (groupings of sitemaps) and sitemaps themselves. These indices and the generation of multiple sitemaps are essential, because a single sitemap can only contain a limited number of pages (50,000) and be of a certain size (under 50MB). This is all taken care of automatically, which allows your site to be discoverable no matter its scale.

## Location

The relevant sitemaps-related links for your instance are found (at the root of your instance's domain/URL prefix):

- **Sitemap indices**: `/sitemap_index_<int:page>.xml`
- **Sitemaps**: `/sitemap_<int:page>.xml`

`<int:page>` is zero-indexed.

Knowing these links becomes relevant if you want to pass them to a search engine's search console manually. In this case, you will typically only have to pass the `/sitemap_index_0.xml` link (as a full canonical URL). This is because a single sitemap index file refers to `SITEMAP_MAX_ENTRY_COUNT` (10,000 by default) sitemap files and each of them to that same number of pages (for a total of 100 million pages by default).

However, InvenioRDM's `robots.txt` links to these URLs, so that they can be automatically detected without manual intervention.

## Configuration

[invenio-sitemap](https://github.com/inveniosoftware/invenio-sitemap) is the main hub for this feature of InvenioRDM. You can find the configurations and more technical details there.

- `SITEMAP_MAX_ENTRY_COUNT` sets the maximum number of entries (`url` or `sitemap`) per file.
- `SITEMAP_SECTIONS`, filled out by default by `invenio-app-rdm`, contains the generators of sitemap entries — instances of `invenio_sitemap.sitemap.SitemapSection`.

Creating custom subclasses of [`SitemapSection`](https://github.com/inveniosoftware/invenio-sitemap/blob/master/invenio_sitemap/sitemap.py), overriding the [templates for the sitemap files](https://github.com/inveniosoftware/invenio-sitemap/tree/master/invenio_sitemap/templates/invenio_sitemap) (as described in [Change templates](./look-and-feel/templates.md)), and changing the above configuration values give you full control over your sitemaps.
