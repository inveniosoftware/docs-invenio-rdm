# Cleanup after you

## Destroy the instance

Finally, we want to destroy it. This will take us to a clean state. Note that it destroys images, containers and volumes (the ones defined in the `december-release/docker-compose.full.yml`. ).

Stop the application:

``` console
(your-virtualenv)$ invenio-cli destroy --containers
Destroying RDM application...
```
