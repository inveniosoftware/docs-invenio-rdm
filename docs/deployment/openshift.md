# OpenShift

## Pre-Requirements

- [Global deployment pre-requirements](index.md#pre-requirements)
- [OpenShift CLI](https://docs.openshift.com/container-platform/4.3/cli_reference/openshift_cli/getting-started-cli.html#cli-installing-cli_cli-developer-commands) version 3.11+


## Deploying InvenioRDM

First of all, log in and select the right project in your OpenShift cluster:

```console
$ oc login <your.openshift.cluster>
$ oc project invenio
```

### Secrets

Before deploying, you need to provide the credentials so the application can access the different services. Replace the credentials and configuration below with your own:

**Invenio secret key**:

  ```console
 $ SECRET_KEY=$(openssl rand -hex 8)
 $ oc create secret generic \
   --from-literal="INVENIO_SECRET_KEY=$SECRET_KEY" \
   invenio-secrets
 ```

**Database secrets:**

```console
$ POSTGRESQL_PASSWORD=$(openssl rand -hex 8)
$ POSTGRESQL_USER=invenio
$ POSTGRESQL_HOST=db
$ POSTGRESQL_PORT=5432
$ POSTGRESQL_DATABASE=invenio
$ oc create secret generic \
  --from-literal="POSTGRESQL_PASSWORD=$POSTGRESQL_PASSWORD" \
  --from-literal="SQLALCHEMY_DB_URI=postgresql+psycopg2://$POSTGRESQL_USER:$POSTGRESQL_PASSWORD@$POSTGRESQL_HOST:$POSTGRESQL_PORT/$POSTGRESQL_DATABASE" \
  db-secrets
secret "db-secrets" created
```

**RabbitMQ secrets:**

```console
$ RABBITMQ_DEFAULT_PASS=$(openssl rand -hex 8)
$ oc create secret generic \
  --from-literal="RABBITMQ_DEFAULT_PASS=$RABBITMQ_DEFAULT_PASS" \
  --from-literal="CELERY_BROKER_URL=amqp://guest:$RABBITMQ_DEFAULT_PASS@mq:5672/" \
  mq-secrets
secret "mq-secrets" created
```

**Elasticsearch secrets:**

!!! info "Elasticsearch variables"
    Currently, and until [invenio-search#198](https://github.com/inveniosoftware/invenio-search/issues/198) has been addressed, the Elasticsearch configuration
    has to be loaded in a single environment variable.

``` console
$ export INVENIO_SEARCH_ELASTIC_HOSTS="[{'host': 'localhost', 'timeout': 30, 'port': 9200, 'use_ssl': True, 'http_auth':('USERNAME_CHANGEME', 'PASSWORD_CHANGEME')}]"
$ oc create secret generic \
  --from-literal="INVENIO_SEARCH_ELASTIC_HOSTS=$INVENIO_SEARCH_ELASTIC_HOSTS" \
  elasticsearch-secrets
```

!!! info "Extra configuration is possible"
    Note that you might need to add extra configuration to the Elasticsearch hosts, such as certificate verification (`verify_certs`), prefixing (`url_prefix`) and more.

### Install InvenioRDM

Before installing you need to configure two things in your `values.yml` file. The rest are optional and you can read more about them [here](configuration.md):

- The host.
- The web/worker docker images.

``` yaml
host: yourhost.localhost

web:
  image: your/invenio-image

worker:
  image: your/invenio-image
```

!!! info "Image registries"
    You can get to know more about where and how to store you instance's docker image [here](./registries).

The next step is the installation itself, with your own configuration in the `values.yaml`. If you added the repository, you can install it by using the chart name and the desired version:

``` console
$ helm install -f values.yaml invenio helm-invenio/invenio --version 0.2.0
```

If you want to install from GitHub, in a clone you can do so as follows:

``` console
$ cd helm-invenio/
$ helm install -f values.yaml invenio ./invenio [--disable-openapi-validation]
```

In both cases the output will be:

``` console
NAME: invenio
LAST DEPLOYED: Mon Mar  9 16:25:15 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:Invenio is ready to rock :rocket:
```

!!! warning "Bypassing openapi validation"
    We must pass `--disable-openapi-validation` as there is currently a problem with OpenShift objects and Helm when it comes to client side validation, see [issue](https://github.com/openshift/origin/issues/24060).


### Setup the instance

Once the instance has been installed you have to set up the services. Note that this step is only needed the first time, if you are upgrading the instance this is not needed.

Get a bash terminal in a web pod:

```console
$ oc get pods
$ oc exec -it <web-pod> bash
```

Setup the instance using the `invenio` commands:

``` console
$ . scl_source enable rh-python36
$ invenio db init # If the db does not exist already, otherwise `create` is enough
$ invenio db create
$ invenio index init
$ invenio index queue init purge
$ invenio files location --default 'default-location'  $(invenio shell --no-term-title -c "print(app.instance_path)")'/data'
$ invenio roles create admin
$ invenio access allow superuser-access role admin
```

#### Launching jobs

**One time job**

In some cases you might want to run jobs, for example to populate the instance with records.

``` console
$ oc process -f job.yml --param JOB_NAME='demo-data-1' \
  --param JOB_COMMAND='invenio rdm-records demo' | oc create -f -
```

**Cron job**

Now, imagine you have some bulk record indexing, or any other task that you have to do periodically.

For that, you can define cronjobs:

``` console
$ oc process -f cronjob.yml --param JOB_NAME=index-run \
  --param JOB_COMMAND=invenio index run -d | oc create -f -
```

### Upgrade your instance

If you have performed some changes to your instance (e.g. configuration) or you want to upgrade the version of the chart, you can do so with
the `upgrade` command of `helm`.

!!! warning "Not supported yet"
    Note that you still need to disable the openapi validation which is not supported yet in version 3.1.2 (However, it is merged into the master branch and should come out soon). For now we will have to `helm uninstall` and then install again.

``` console
$ helm upgrade -f values.yaml --disable-openapi-validation
```
