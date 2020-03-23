# Configuration

This section explains the current configuration options that are available for the different components deployed by this Helm chart.

## Global

There is only one mandatory configuration: the host name.

```yaml
host: your-rdm-instance.com
```

Moreover, the services can be deployed along. Note that it is recommended to deploy Elasticsearch and PostgreSQL separately for a production deployment.
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

You can change the number of connections allowed by haproxy with the `maxconn` variable:

```
haproxy:
  maxconn: 100
```

## Nginx

This chart allows you to configure the amount of connections per nginx node (replica) and the amount of nodes:

```
nginx:
  max_conns: 100
  replicas: 2
```

## Web nodes

The web nodes host the WSGI application. In order to be scalable you can configure the number of "nodes", called replicas, with how many processes each node runs and with how many threads per process. The only mandatory parameter is the docker image (`image`) that should get as value the url where to pull the image from.

In addition, you can add automatic scaling by setting minimum (`min_web_replicas`) and maximum (`max_web_replicas`) replicas, and the cpu usage threshold in percentage (`scaler_cpu_utilization`) that spawns a new node. For example, with a `scaler_cpu_utilization` value of 65, it means that when the average CPU utilization of the nodes reaches 65%, a new node will be spawned. This process will repeat itself until the maximum number of replicas has been reached:

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

Finally, the worker nodes. By default they are enabled, but you can cancel their deployment by setting `enabled` to `false`. If enabled, they require an `image` like the web nodes.

In addition, you can configure the number of worker nodes (replicas) to be deployed, the application they will run, their concurrency level and their logging level.

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
