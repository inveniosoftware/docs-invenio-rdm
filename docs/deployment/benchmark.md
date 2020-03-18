# Benchmarking your Invenio instance

The operations that we are going to run in this section can be highly
demanding. Therefore, you might not want to run them against a production
instance since it might cause downtime.

Nonetheless, we want to have an environment that resembles as close as
possible to our InvenioRDM instance. In consequence, we might want to add some
data to our instance in order to have some records to stress-test against.

## Populate your instance

!!! info "Already populated instances"
    If you already have content in the instance this step is not needed.

We are going to create some demo records using a new CLI command.
We are going to use `invenio` commands. You can lunch a job using the
[provided job templates](https://github.com/inveniosoftware/helm-invenio/tree/master/jobs)
(recommended) or execute them in a web container's terminal.

!!! warning "OpenShift commands"
    The following commands assume you are using OpenShift. For bare
    Kubernetes, commands might be slightly different.

**Launch a job**

You will need to either download the file from [here](https://github.com/inveniosoftware/helm-invenio/tree/master/jobs)
or go to the `jobs` folder if you have the [helm-invenio](https://github.com/inveniosoftware/helm-invenio)
repository cloned in your machine.

The following job will be executed by a worker and create 10 demo records.

``` console
$ oc process -f job.yml --param JOB_NAME='demo-data' \
  --param JOB_COMMAND='invenio rdm-records demo' | oc create -f -
```

**Execution in a web container**

To populate the instance with the alternative method, you need to connect to a
running pod, activate python3 and execute the command:

```console
$ oc get pods # List all pods
$ oc exec -it <web-pod-id> bash # Connect to a web pod
$ . scl_source enable rh-python36 # Activate python3
$ invenio rdm-records demo # Create 10 demo records
```

This methods populate the instance with 10 records. If you need more, you can
run it multiple times. However, obtaining a high number of records might be
time consuming with this method. In that case, you can use bulk indexing, you
can find more documentation on how to do it [here](https://github.com/inveniosoftware/helm-invenio/tree/master/benchmark#populate-your-instance).

## Benchmark

In order to test the load that your instance is able to stand, you can use
[Locust](https://docs.locust.io/en/stable/). [Here](https://github.com/inveniosoftware/helm-invenio/blob/master/benchmark/locustfile.py)
you can find a `locustfile.py` file ready to test an Invenio instance. Let's
test it!

First install locust:

``` console
$ pip install locust
```

The given locust file makes use of some values that you might want to
adjust to your instance:

``` python
RECID = 'h2kh0-vfq12'
NON_EXISTING_RECID = 9999
SEARCH_QUERY = "Baker"
```

`RECID` represents the ID of a record that exists in the instance, while
`NON_EXISTING_RECID` represents one that doesn't. Finally, `SEARCH_QUERY`
should contain a string that matches a limited amount of records. The
purpose of this query is to test when only certain records are returned.
A full query (i.e. all records) is also tested.

Then, in order to lunch the tests you need to be in the directory where the
`locustfile.py` is:

``` console
$ curl https://raw.githubusercontent.com/inveniosoftware/helm-invenio/master/benchmark/locustfile.py \
  -o /path/where/to/save/locustfile.py
$ cd /path/where/to/save/
$ locust
```

Once it is running, you can navigate to [the web interface](http://localhost:8089)
and set the amount of users/and users joining per second. Play with these
numbers until you reach the number of requests per second (shown in the top
right) that you are looking for.
