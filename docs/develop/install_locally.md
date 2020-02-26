# Install Locally

In the [Preview Section](../preview/index.md), we have been running all of the
application in docker containers. This saves you the trouble of installing the
instance on your host and gets something visible fast. Now, we will run the
application locally and the database and other services in containers. It's the
best compromise between getting up and running with relevant services fast, while
allowing you to iterate on your local instance quickly.

Before going on, let's move into the project directory:

``` console
$ cd february-release-2
```

To run the application locally, we will need to install it and its dependencies
first. We do not need to add `--pre`, since we do not have to install any alpha releases. Nonetheless, this option is still available if you need it. Be patient, it might take some time to build.


``` console
$ invenio-cli install
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

We need to initialize the database, the indices and so on. For this, we can use
the `services` command. Note that this command is only needed once. Afterwards, you
can stop (not destroy) these services and start again, and your data will still be there.

``` console
$ invenio-cli services
Making sure containers are up...
Creating database...
Creating indexes...
Creating files location...
Creating admin role...
Assigning superuser access to admin role...
```

In case you want to wipe out the data that was there (say to start fresh),
you can use `--force` and nuke the content!

``` console
$ invenio-cli services --force
Making sure containers are up...
Flushing redis cache...
Deleting database...
Deleting indexes...
Purging queues...
Creating database...
Creating indexes...
Creating files location...
Creating admin role...
Assigning superuser access to admin role...
```

**Known issues**:

The Elasticsearch container might crash due to lack of memory. One solution is to increase the maximum allowed allocation per process (See more [here](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/docker.html)). Solving this issue depends on your OS:

On Linux, add the following to ``/etc/sysctl.conf`` on your local machine (host machine):

```console
# Memory mapped max size set for ElasticSearch
vm.max_map_count=262144
```

On macOS, do the following:

```console
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
# and in the shell
sysctl -w vm.max_map_count=262144
```

## Populate DB

Let's add some content so you can interact a bit with the instance. For this
you will generate 10 random demo records, using the `demo` command:

``` console
$ invenio-cli demo --local
Making sure containers are up...
Populating instance with demo records...
```

We are ready to run it in the next section.