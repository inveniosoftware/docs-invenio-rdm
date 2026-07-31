# Switching to rspack

Can be skipped without performing any change if not switching.

We recommend switching from `webpack` to
[Rspack](https://www.rspack.dev/) for asset bundling. Its Rust-based
builds are much faster and drop-in compatible with the existing
Invenio asset pipeline. In your `invenio.cfg`:

```python
WEBPACKEXT_PROJECT = "invenio_assets.webpack:rspack_project"
```

If you want to use `rspack` in your Docker image you have to add it to
`Dockerfile` too.
