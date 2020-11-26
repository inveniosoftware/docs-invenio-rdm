# Cleanup after you

## Stop the instance

We have reached the end of this journey, we are going to stop the instance. This will **NOT** destroy images, containers or volumes i.e. your data will be preserved.

``` bash
^C
Stopping server and worker...
Server and worker stopped...
```

If you wish to stop the service containers without destroying them nor wiping their content, use the `stop` command:

```bash
invenio-cli services stop
```

## Destroy the instance

If you want to get to a clean state with no images, containers or volumes, then destroy the instance. This **WILL** permanently erase your volume data (database and Elasticsearch indices).
It destroys the images, containers and volumes defined in the `development-instance/docker-compose.full.yml`.

After stopping the application per above, destroy it:

``` bash
invenio-cli services destroy
```

If you also want to destroy a pipenv managed virtual environment along with the containers you can use the global `destroy command`:

```bash
invenio-cli destroy
```