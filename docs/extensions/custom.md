# Extensions

If you want to add custom functionality to your RDM instance, you need to develop your own module. You can start in no time by using the [cookiecutter-invenio-module](https://github.com/inveniosoftware/cookiecutter-invenio-module) template.

## Create your module
Let's run the cookiecutter:

``` bash
cookiecutter https://github.com/inveniosoftware/cookiecutter-invenio-module
```

## Add your functionality

We've added a simple view to the blueprint in `<your_custom_module>/views.py`, which looks like:

``` python
# Other code ignored for clarity

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

``` bash
cd path/to/your/instance
pipenv install [--pre] -e path/to/your/extension
```

As you can see, `--pre` is optional. It is only needed when the package is in a pre-release state. In addition, note that you do not need to specify a local path. If the package is available e.g. via PyPi, you can just install it by its name.

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

``` bash
invenio-cli run
```

!!! note "UI related extensions"
    If your extension adds scss and/or javascript, you will need to update your final static files before running your instance! You can do so with the CLI: `invenio-cli update [--no-install-js]`