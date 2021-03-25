# Stop or destroy your instance

## Stoping containers

If you want to temporarily stop the instance without losing the data that
was generated, you can use the `stop` command:

```bash
invenio-cli containers stop
# or
invenio-cli services stop
```

## Destroying containers

!!! warning
    The ``destroy`` command WILL permanently erase all your data in the Docker containers.


On the other hand, if you wish to clean up and delete all Docker artefacts,
you can use the `destroy` command. It removes all containers, images and volumes.

Note that `destroy` will also `stop` the containers, so there is no need to run the previous command:


```bash
invenio-cli containers destroy
# or
invenio-cli services destroy
```

## Destroying all

If you also want to destroy a pipenv managed Python virtual environment along with the containers you can use the global `destroy command`:

```bash
invenio-cli destroy
```
