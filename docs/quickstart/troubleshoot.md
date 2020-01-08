# Troubleshooting

Something has gone wrong, now what? InvenioRDM provides logs in two ways, depending on where the error happened. If the error comes from the deployment of the instance (e.g. the containerized quickstart or a local development instance) your section is the [CLI](#cli) on the other hand, if once the application is running you get an error you should go to the [Web Application](#web-application) section.

## CLI

The Invenio-CLI saves the logs in the `logs` folder, inside the directory that was created with your instance name. For example, if you called it `My Site`, the logs file would be `my-site/logs/invenio-cli.log`.

``` console
(your-virtualenv)$ invenio-cli init --flavour=RDM
Initializing RDM application...
You've downloaded /home/youruser/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:
project_name [My Site]: My Site
project_shortname [my-site]: my-site <-- *THIS IS THE NAME OF THE FOLDER*
...
```

Another option is to run the CLI in verbose mode and get all the logs in the terminal at the same time thatn you execute the commands. To do so, just add the `--verbose` option to the commands. For example: `invenio-cli setup --versbose --containers`.

## Web Application

If you are running a development (`--local`) InvenioRDM instance you can use the `--verbose` flag in order to get the logs forwareded to the terminal. However, if you are running the containerized environment you need to get the logs from the corresponding containers. It can be done in two steps, first obtaining the container IDs and then getting their logs:

``` console
$ docker ps -a

CONTAINER ID        IMAGE                                                     COMMAND                  CREATED             STATUS                           PORTS                                                                                        NAMES
5cb64814ed2a        my-site-frontend                                          "nginx -g 'daemon of…"   24 minutes ago      Up 1 minute                                                                                                                   mysite_frontend_1
39993dcbb84f        my-site                                                   "bash -c 'celery wor…"   24 minutes ago      Up 1 minute                                                                                                                   mysite_worker_1
ff9a589845e4        my-site                                                   "bash -c 'uwsgi /opt…"   24 minutes ago      Up 1 minute                      0.0.0.0:32810->5000/tcp                                                                      mysite_web-api_1
a99532c10a8b        my-site                                                   "bash -c 'uwsgi /opt…"   24 minutes ago      Up 1 minute                      0.0.0.0:32811->5000/tcp                                                                      mysite_web-ui_1
d9afc36a573c        redis                                                     "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      0.0.0.0:6379->6379/tcp                                                                       mysite_cache_1
cbdac8cbd6a9        rabbitmq:3-management                                     "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   mysite_mq_1
38d63e050e6b        postgres:9.6                                              "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      0.0.0.0:5432->5432/tcp                                                                       mysite_db_1
30356839105a        docker.elastic.co/elasticsearch/elasticsearch-oss:7.2.0   "/usr/local/bin/dock…"   24 minutes ago      Up 3 minute (health: starting)   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp                                               mysite_es_1
```

The most insteresting ones will be the `web-ui` and `web-api` containers, which in this case have id `a99532c10a8b` and `ff9a589845e4` respectively. The logs can be obtaines by using the `logs` command of `docker`. An example of a working instance of the `web-api` container would show the following (Trimmed output for clarity):

``` console
$ docker logs ff9a589845e4

[uWSGI] getting INI configuration from /opt/invenio/var/instance/uwsgi_rest.ini
*** Starting uWSGI 2.0.18 (64bit) on [Wed Jan  8 13:09:07 2020] ***
[...]
spawned uWSGI master process (pid: 1)
spawned uWSGI worker 1 (pid: 255, cores: 2)
spawned uWSGI worker 2 (pid: 257, cores: 2)
*** Stats server enabled on 0.0.0.0:9001 fd: 11 ***
```


              