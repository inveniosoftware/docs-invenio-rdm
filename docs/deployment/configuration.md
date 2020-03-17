# Configuration

This section explain the current configuration options that are available for the different components that are deployed but the Helm charts.

## Global

The is only one mandatory configuration, which is the host name, for example:

```yaml
host: your-rdm-instance.com
```

Moreover, the services can be deployed along, note that it is recommended to deploy separatelly Elasticsearch and PostgreSQL for a production deployment.
Therefore, by default only `redis` and `rabbitmq` are enabled. Example configuration:

``` yaml
postgresql:
  inside_cluster: false

elasticsearch:
  inside_cluster: false
```

!!! info "inside_cluster availability
    Note that the `inside_cluster` variable is supported for `redis`, `rabbitmq`, `elasticsearch`, `postgresql` and `haproxy`. The rest of the components
    are mandatory.

## HAProxy

You can change the number of connections allowed by the haproxy with the `maxconn` variable:

```
haproxy:
  maxconn: 100
```

!!! warning "Only one parent element"
    By default the HAProxy is enabled, `inside_cluster` has the value `true`, nonetheless if you decide to set it, you only need
    to specify once the `haproxy` parent in the yaml file. Otherwise the last one will override the previous. It should be something like:
    ``` yaml
    haproxy:
        inside_cluster: true
        maxconn: 100
    ```
## Nginx

The charts allow you to configure the amount of connections per nginx node (replica) and the amount of nodes:

```
nginx:
  max_conns: 100
  replicas: 2
```

## Web nodes

The web nodes host the WSGI application, in order to be scalable you can configure the number of "nodes", called replicas, how many processes do each node run and with how many threads per process. The only mandatory parameter is the docker image (`image`) that should get as value the url where to pull the image from.

In addition, you can add automatic scaling, by setting minimum and maximum replicas and the threshold of cpu usage in which a new node should be spawned. For example, with a threshold of 65%, it meand that when the average CPU utilization of the nodes reaches 65% a new node will de spawned, till it reaches the setted maximum:

``` yaml
web:
  image: your/invenio-image
  replicas: 6
  uwsgi:
    processes: 6
    threads: 4
  autoscaler:
    enabled: false
    # Scale when CPU usage gets to
    scaler_cpu_utilization: 65
    max_web_replicas: 10
    min_web_replicas: 2
```

## Worker nodes

Finally, the worker nodes. By default they are enabled, but you can cancel their deployment by setting `enabled` to `false`. If enabled, in the same fashion than the web nodes
they require an `image`.

In addition, you can configure how many worker nodes (replicas) will be deployed, which the application they will run, with which concurrency level and the logging level.

``` yaml
worker:
  enabled: true
  image: your/invenio-image
  # Invenio Celery worker application
  app: invenio_app.celery
  # Number of concurrent Celery workers per pod
  concurrency: 2
  log_level: INFO
  replicas: 2
  ```
