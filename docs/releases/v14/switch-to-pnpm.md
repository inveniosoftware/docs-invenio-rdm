# Switch from npm to pnpm

[Pnpm](https://pnpm.io/) is now the recommended tool to manage
Javascript dependencies in InvenioRDM (don't worry npm still works)
because it is much faster, [has better protection against supply chain
attacks](https://pnpm.io/supply-chain-security), and has good
community support. If you have it installed, `invenio-cli` and lower
level `invenio` commands will use it under the hood (if installed).

1.  Locally, install [pnpm](https://pnpm.io/installation) version 11 (working version at time of writing).

2.  Make sure to set "pnpm" as your invenio javascript package manager in `.invenio`.

    ```ini
    [cli]
    # set this line or remove it altogether
    javascript_package_manager = pnpm
    ```

    You could remove the line altogether since pnpm is the new default if that line is not present.

3.  In your `invenio.cfg`, set:

    ```python
    WEBPACKEXT_NPM_PKG_CLS = "pynpm:PNPMPackage"
    ```

    to make sure pnpm is used by assets building commands inside and outside your containers.

That's it, faster JavaScript package resolutions are yours now!

### Not switching to pnpm

You can keep using npm to manage JS dependencies. To do so, verify that the following are set:

1.  "npm" is set as your invenio javascript package manager in `.invenio`.

    ```ini
    [cli]
    javascript_package_manager = npm
    ```

2.  In your `invenio.cfg`, set:

    ```python
    # The default is "pynpm:NPMPackage" but may change in a future major version
    WEBPACKEXT_NPM_PKG_CLS = "pynpm:NPMPackage"
    ```
