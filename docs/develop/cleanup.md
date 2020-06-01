# Cleanup after you

## Stop the instance

We have reached the end of this journey, we are going to stop the instance. This will **NOT** destroy images, containers or volumes i.e. your data will be preserved.

``` bash
^C
Stopping server and worker...
Server and worker stopped...
```

## Destroy the instance

If you want to get to a clean state with no images, containers or volumes, then destroy the instance. This **WILL** permanently erase your volume data (database and Elasticsearch indices).
It destroys the images, containers and volumes defined in the `development-instance/docker-compose.full.yml`.

After stopping the application per above, destroy it:

!!! warning "Temporarily unavailable"
    The destroy command is temporarily unavailable. We are sorry for the inconvenience.

``` bash
invenio-cli destroy
```
```console
TODO: Revisit destroy command...
```
