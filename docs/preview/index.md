# Quick preview of InvenioRDM

Now that you have `invenio-cli` [installed](../install/index.md), we will use
it to give you a very quick preview of InvenioRDM. We will initialize an
InvenioRDM project and run a fully containerized local instance. This way, you
can see for yourself how simple it is to get started and what an InvenioRDM
instance looks like.

## Initialize your file system

First, we need to create the project - the necessary files and folders for your InvenioRDM instance.

The CLI will require the following data:

- **Project name**: Title of your project with space allowed (project name for humans)
- **Project short name**: Hyphenated and lowercased title (project name for machines)
- **Project website**: URL where the project will be deployed
- **GitHub repository**: Repository in format `<owner>/<code repository>`
- **Description**: Short description of project
- **Author name**: Your name or that of your organization
- **Author email**: Email for communication
- **Year**: The current year
- **Python version**: 3.7 (default), 3.6, and 3.8 (beta).
- **One of the three available storage systems**: postgresql (default), mysql or sqlite
- **The version of Elasticsearch**: 7 (default) or 6
- **Storage backend**: Local file system (default) or in a S3-like backend. If S3 is chosen a MinIO container is provided, however, you can set it up to use your own. See more in [S3 extension](../extensions/s3.md)

It will also generate a test private key.

Let's do it! Pressing `[Enter]` selects the option in brackets `[]`.

``` bash
invenio-cli init rdm
```

``` console
Initializing RDM application...
Running cookiecutter...
project_name [My Site]: InvenioRDM Preview
project_shortname [inveniordm-preview]:
project_site [inveniordm-preview.com]:
github_repo [inveniordm-preview/inveniordm-preview]:
description [Invenio RDM InvenioRDM Preview Instance]:
author_name [CERN]:
author_email [info@inveniordm-preview.com]:
year [2020]:
Select python_version:
1 - 3.7
2 - 3.6
3 - 3.8 (beta)
Choose from 1, 2, 3 [1]:
Select database:
1 - postgresql
2 - mysql
3 - sqlite
Choose from 1, 2, 3 [1]:
Select elasticsearch:
1 - 7
2 - 6
Choose from 1, 2 [1]:
Select file_storage:
1 - local
2 - S3
Choose from 1, 2 [1]:
-------------------------------------------------------------------------------

Generating SSL certificate and private key for testing....
Generating a RSA private key
..................++++
..................................++++
writing new private key to 'docker/nginx/test.key'
-----
-------------------------------------------------------------------------------
Creating logs directory...
```

Observe the generated files. A full description of each of them can be found in the [invenio-cli RFC](https://github.com/inveniosoftware/rfcs/pull/4)

``` bash
ls -la inveniordm-preview
```
``` console
total 56
drwxr-xr-x 5 youruser youruser 4096 Feb 19 13:45 ./
drwxr-xr-x 5 youruser youruser 4096 Feb 19 13:45 ../
drwxr-xr-x 3 youruser youruser 4096 Feb 19 13:45 app_data/
drwxr-xr-x 3 youruser youruser 4096 Feb 19 13:45 assets/
drwxr-xr-x 4 youruser youruser 4096 Feb 19 13:45 docker/
-rw-r--r-- 1 youruser youruser 2932 Feb 19 13:45 docker-compose.full.yml
-rw-r--r-- 1 youruser youruser  943 Feb 19 13:45 docker-compose.yml
-rw-r--r-- 1 youruser youruser 2665 Feb 19 13:45 docker-services.yml
-rw-r--r-- 1 youruser youruser 1152 Feb 19 13:45 Dockerfile
-rw-r--r-- 1 youruser youruser   46 Feb 19 13:45 .dockerignore
-rw-r--r-- 1 youruser youruser 2018 Feb 19 13:45 .invenio
-rw-r--r-- 1 youruser youruser 2018 Feb 19 13:45 .invenio.private
-rw-r--r-- 1 youruser youruser 1504 Feb 19 13:45 invenio.cfg
drwxr-xr-x 2 youruser youruser 4096 Feb 19 13:45 logs/
-rw-r--r-- 1 youruser youruser  431 Feb 19 13:45 Pipfile
-rw-r--r-- 1 youruser youruser  756 Feb 19 13:45 README.md
drwxr-xr-x 3 youruser youruser 4096 Feb 19 13:45 static/
drwxr-xr-x 2 youruser youruser 4096 Feb 19 13:45 templates/
```

#### Notes and Known Issues

- For now, the only available flavour is RDM (Research Data Management). In the future, there will be others, for example ILS (Integrated Library System).

- You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:`. Press `[Enter]` in that case. This will download the latest cookiecutter template.

- Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.


## Preview instance

!!! warning "NEW: Adjust `SITE_HOSTNAME`"
    New in the October release: the `SERVER_HOSTNAME` configuration variable is now called `SITE_HOSTNAME`
    and can be modified in `invenio.cfg` or using the `INVENIO_SITE_HOSTNAME` environment variable.

#### Set SITE_HOSTNAME

This is required because `invenio-cli init rdm` generates a config file (`invenio.cfg`)
for [development usage](../develop/index.md) by default. We need to tweak it,
because we are only previewing InvenioRDM.

Before running your instance, change the following in `invenio.cfg`:

```diff
- SITE_HOSTNAME = "127.0.0.1:5000"
+ SITE_HOSTNAME = "127.0.0.1"
```

Alernatively, you can export it in your environment. If you do so, remember to prefix it with `INVENIO_`.

Using a bash shell:

```bash
export INVENIO_SITE_HOSTNAME="127.0.0.1"
```

Using a fish shell:

```fish
set --export INVENIO_SITE_HOSTNAME "127.0.0.1"
```

#### Containerize and run

The project is initialized, we now run it. Switch to the project
directory and do so:

``` bash
cd inveniordm-preview
invenio-cli containerize --pre
```
``` console
<... build output ignored ...>
Instance running!
Visit https://127.0.0.1
```
``` bash
firefox https://127.0.0.1
```

!!! warning "Use 127.0.0.1"
    Due to Content Security Policy (CSP) headers it is important that you use 127.0.0.1, and not localhost. Unless you set the `SITE_HOSTNAME` to localhost.

#### Notes and Known Issues

- You may see the following error message `TypeError: Object.fromEntries is not a function`.
  This means you need to update your base Invenio docker image because Node.js 14+ is needed.
  Run `docker pull inveniosoftware/centos7-python:3.6` or `docker pull inveniosoftware/centos8-python:3.7` (or python 3.8)  before running `invenio-cli containerize --pre` again.
- You may see `SystemError: Parent module 'setuptools' not loaded, cannot perform relative import`
  at the dependency locking step when running `invenio-cli containerize --pre`. This depends on your version of `setuptools` (bleeding edge causes this)
  and can be solved by setting an environment variable: `SETUPTOOLS_USE_DISTUTILS=stdlib`. [See more details](https://github.com/pypa/setuptools/blob/17cb9d6bf249cefe653d3bdb712582409035a7db/CHANGES.rst#v5000). This sudden upstream change will be addressed more systematically in future releases.

## Add random records

You now have a running instance of InvenioRDM at [https://127.0.0.1](https://127.0.0.1),
but it doesn't have any records in it. For demonstration purposes, we will add
randomly generated records:

``` bash
invenio-cli demo --containers
```

You can now get a full sense for what InvenioRDM offers. Explore!


## Running Invenio commands

If you are already familiar with Invenio and the many commands its CLI (`invenio`)
provides, you might be wondering how to execute those. Because the entire application
is containerized, you need to connect to the web-api or web-ui container in order
to use one of those commands. In fact, this is what `invenio-cli` does behind the scene!

``` bash
docker-compose --file docker-compose.full.yml exec web-ui /bin/bash -c "invenio <your command>"
```


## Stop it

If you want to temporarily stop the instance without losing the data that
was generated, you can use the `stop` command:

```bash
invenio-cli stop
```

On the other hand, if you wish to clean up and delete all Docker artefacts,
you can use the `destroy` command. It removes all containers, images and voluments.
Note that `destroy` will also `stop` the containers, so there is no need to run the previous command:

```bash
invenio-cli destroy
```

## Conclusion

In just two commands you can get a preview of InvenioRDM:

``` bash
invenio-cli init rdm
cd <project name>
# Export INVENIO_SITE_HOSTNAME = "127.0.0.1" or set it in invenio.cfg
invenio-cli containerize --pre
invenio-cli stop
```

These instructions don't provide you with a nice development experience though.
You need to run `invenio-cli containerize` for every change you make in your
project. That's slow and cumbersome. Up next, we show how to [develop your
local instance](../develop/index.md) and set yourself up to be productive!
