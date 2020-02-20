# Extensions

If you need to add custom functionalaty to your RDM instance you need to develop your own module. You can start it by using the [cookiecutter-invenio-module](https://github.com/inveniosoftware/cookiecutter-invenio-module) template. It will get you started in no time.

## Create your module
Lets assume you have already done so:

``` console
$ cookiecutter https://github.com/inveniosoftware/cookiecutter-invenio-module

[...]
```

## Add your functionality

And you have added a simple view to the blue print in the `<your_custom_module>/views.py`, which looks like:

``` python
[...]
blueprint = Blueprint(
    'invenio_rdm_extension_demo',
    __name__
)


@blueprint.route("/rdm-ext-demo")
def index():
    """RDM Extension Demo view."""
    return 'RDM Extension Demo!'
```

## Integrate it in your InvenioRDM instance

Once you have your functionality ready, in order to add it to your instance you just have to install the module via pipenv:

``` console
$ cd path/to/your/instance
$ pipenv install [--pre] -e path/to/your/extension
```

As you can see, `--pre` is optional, it is only needed when the package is in a pre-release state. In addition, note that you do not need to specify a local path, if the package is available e.g. via PyPi you can just install it by its name.

## Sanity check and run!

Check that the Pipfile got a new line with your extension. For example:

``` console
...

[packages]
...
invenio-rdm-extension-demo = {editable = true, path="../invenio-rdm-ext-demo"}
...
```

It's all set, run your instance with the cli and you will have your new features available!

``` console
$ invenio-cli run
```
