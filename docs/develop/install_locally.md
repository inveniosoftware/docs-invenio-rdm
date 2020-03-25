# Install Locally

In the [Preview Section](../preview/index.md), we have been running all of the
application in docker containers. This saves you the trouble of installing the
instance on your host and gets something visible fast. Now, we will run the
application locally and the database and other services in containers. It's the
best compromise between getting up and running with relevant services fast, while
allowing you to iterate on your local instance quickly.

Before going on, let's move into the project directory:

``` bash
cd development-instance
```

To run the application locally, we will need to install it and its dependencies
first. We do not need to add `--pre`, since we do not have to install any alpha releases. Nonetheless, this option is still available if you need it. Be patient, it might take some time to build.


``` bash
invenio-cli install
```
``` console
# Summarized output
Installing python dependencies...
Symlinking invenio.cfg...
Symlinking templates/...
Collecting statics and assets...
Installing js dependencies...
Copying project statics and assets...
Symlinking assets/...
Building assets...
```

As a result, the Python dependencies for the project have been installed in
a new virtualenv for the application and many of the files in your project directory
have been symlinked inside it.

## Setup the database, Elasticsearch, Redis and RabbitMQ

We need to initialize the database, the indices and so on. For this, we use
the `services` command. The first time this command is run, the services will be
setup correctly and the containers running them will even restart upon a reboot
of your machine. If you stop and restart those containers, your data will still
be there. Upon running this command again, the initial setup is skipped.


``` bash
invenio-cli services
```
``` console
Making sure containers are up...
Creating network "development-instance_default" with the default driver
Creating development-instance_cache_1 ... done
Creating development-instance_es_1    ... done
Creating development-instance_db_1    ... done
Creating development-instance_mq_1    ... done
Creating database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Creating all tables!
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

!!!note
    You will notice `Making sure containers are up...` like the above and a 30s
    delay in the output of the commands we cover next. This is because they make
    doubly sure the containers are running. In future releases, we will reduce
    this delay.

In case you want to wipe out the data that was there (say to start fresh),
you can use `--force` and nuke the content!

``` bash
invenio-cli services --force
```
``` console
Making sure containers are up...
development-instance_mq_1 is up-to-date
development-instance_db_1 is up-to-date
development-instance_cache_1 is up-to-date
development-instance_es_1 is up-to-date
Cache cleared
Destroying database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Destroying indexes...
Indexing queue has been initialized.
Indexing queue has been purged.
Creating database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Creating all tables!
  [####################################]  100%
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

**Known issues**:

The Elasticsearch container might crash due to lack of memory. One solution is to increase the maximum allowed allocation per process (See more [here](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/docker.html)). Solving this issue depends on your OS:

On Linux, add the following to ``/etc/sysctl.conf`` on your local machine (host machine):

```bash
# Memory mapped max size set for ElasticSearch
vm.max_map_count=262144
```

On macOS, do the following:

```bash
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
# and in the shell
sysctl -w vm.max_map_count=262144
```

## Populate DB

Let's add some content so you can interact a bit with the instance. For this
you will generate 10 random demo records, using the `demo` command:

``` bash
invenio-cli demo --local
```
``` console
Making sure containers are up...
development-instance_mq_1 is up-to-date
development-instance_db_1 is up-to-date
development-instance_cache_1 is up-to-date
development-instance_es_1 is up-to-date
Creating demo records...
Created records!
```

We are ready to run it in the next section.