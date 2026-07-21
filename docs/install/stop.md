# Stop or destroy your instance

## Stop it

If you want to temporarily stop the instance without losing the data that
was generated, you can use the `stop` command:

=== "Local development"

    ```bash
    invenio-cli services stop
    ```

=== "Containerized preview"

    ```shell
    invenio-cli containers stop
    ```

## Destroy it

If you wish to clean up and delete all Docker artefacts,
you can use the `destroy` command. It removes ALL InvenioRDM-related containers, images and volumes.

!!! warning
    The ``destroy`` command WILL permanently erase all your data in the Docker containers.

Note that `destroy` will also `stop` the containers, so there is no need to run the previous command:

=== "Local development"

    ```bash
    invenio-cli services destroy
    ```

=== "Containerized preview"

    ```shell
    invenio-cli containers destroy
    ```

## Destroy everything

If you want to wipe everything (virtual environment, containers, data...) EXCEPT your project files (all files setup by cookiecutter), you can use the global `destroy command`. This command is the same for both installation options:

```bash
invenio-cli destroy
```
