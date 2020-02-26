# Troubleshooting

Something has gone wrong, now what? InvenioRDM provides logs in two ways, depending on where the error happened.
If the error comes from the local development instance (`invenio-cli run`), look at the terminal, the logs show up there.
On the other hand, if the error comes from the fully containerized application (`invenio-cli containerize`), you won't see logs on the terminal directly.
See below.

## Web Application

If you are running the containerized environment you need to get the logs from the corresponding containers. It can be done in two steps, first obtaining the container IDs and then getting their logs:

``` bash
docker ps -a
```
``` console
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

The most interesting ones will be the `web-ui` and `web-api` containers, which in this case have id `a99532c10a8b` and `ff9a589845e4` respectively. The logs can be obtained by using the `logs` command of `docker`. An example of a working instance of the `web-api` container would show the following (trimmed output for clarity):

``` bash
docker logs ff9a589845e4
```
``` console
[uWSGI] getting INI configuration from /opt/invenio/var/instance/uwsgi_rest.ini
*** Starting uWSGI 2.0.18 (64bit) on [Wed Jan  8 13:09:07 2020] ***
[...]
spawned uWSGI master process (pid: 1)
spawned uWSGI worker 1 (pid: 255, cores: 2)
spawned uWSGI worker 2 (pid: 257, cores: 2)
*** Stats server enabled on 0.0.0.0:9001 fd: 11 ***
```
