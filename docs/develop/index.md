# Develop

Customization might not be enough for you. Perhaps you need to write custom functionality as part of an extension.
Or perhaps you are implementing a feature or fixing a bug in a core InvenioRDM module.
The point is that you need to install a module from a local path
and see the changes reflected on your instance.

## Develop a local module

Get to know how to install a module as part of an instance for local development.

[> Develop or edit a module](develop.md)

## Use existing extensions

InvenioRDM supports a great variety of extensions that can help you adapt it to your infrastructure. The currently supported extensions are listed below.

- [S3](s3.md) can be configured to serve as your storage backend via the [invenio-s3](https://github.com/inveniosoftware/invenio-s3) extension. If you chose S3 as storage when initializing your instance, [navigate here](#i-chose-s3-when-initializing-the-repository). Otherwise, [navigate to this section](#i-didnt-choose-s3-when-initializing).

- [MeSH](https://github.com/galterlibrary/invenio-subjects-mesh) can be installed to have subjects support for topical [Medical Subject Headings](https://www.ncbi.nlm.nih.gov/mesh/).

## Create your own extensions

If no existing extensions suit your needs, you may want to create your own extension to add custom functionality to your RDM instance. We have the docs and cookiecutter template to get you started in no time.

[> Develop an extension](custom.md)
