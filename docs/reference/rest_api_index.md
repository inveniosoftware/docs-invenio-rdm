# REST API reference

**Summary**

The following document is a reference guide for all the REST APIs that InvenioRDM exposes.

**Intended audience**

This guide is intended for advanced users, and developers of InvenioRDM that have some experience with using REST APIs and are aware of the expected functionality a repository would be exposing.

## Authentication

The only authentication method supported at the moment for REST API calls is by using Bearer tokens that you can generate at the "Applications" section of your user account's settings of your InvenioRDM instance. There are two ways to pass the tokens in your requests.

**Authorization HTTP header (recommended)**

```shell
curl -k -H "Authorization: Bearer API-TOKEN" https://127.0.0.1:5000/api/records
```

**`access_token` HTTP query string parameter**

```shell
curl -k https://127.0.0.1:5000/api/records?access_token=API-TOKEN
```

!!! info "Insecure connection"
    The `-k` or `--insecure` option here is simply because a certificate is typically not setup locally. In production,
    your `curl` calls shouldn't need this option because you will be using a valid certificate.

### Scopes

!!! warning "Work in progress"

    The available scopes for generated token are subject to change when the access control mechanisms to records are finalized.

When you create your API token you can also specify **scopes** that control what kind of resources and actions you can access using your token.

| Scope        | Description                               |
| ------------ | ----------------------------------------- |
| `user:email` | Allows access to the user's email address |

Bear in mind, `user:email` is the only scope that exists by default. If you require further customization, consider [customizing your authentication](../customize/authentication.md#oauth) and [delegating rights via scopes](https://invenio-oauth2server.readthedocs.io/en/latest/usage.html#delegating-rights-via-scopes).

## General information

### Example

We provide an example of how to upload a record with files to an InvenioRDM
instance in the following [repository](https://github.com/inveniosoftware/docs-invenio-rdm-restapi-example).

### Timestamps

Timestamps are in UTC and formatted according to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

### Pretty print JSON

If you are exploring the API via a browser, you can have the JSON formatted by
adding ``prettyprint=1`` in the query string.

**Example request**

```http
GET /api/records?prettyprint=1 HTTP/1.1
```
