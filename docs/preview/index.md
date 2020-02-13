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
- **Project short name**: Hyphenated and lowercased title or (project name for machines)
- **Project website**: URL where the project will be deployed
- **Github repository**: Repository in format `<owner>/<code repository>`
- **Description**: Short description of project
- **Author name**: Your name or that of your organization
- **Author email**: Email for communication
- **Year**: The current year
- **One of the three available storage systems**: postgresql (default), mysql or sqlite
- **The version of Elasticsearch**: 7 (default) or 6

It will also generate a test private key.

Let's do it! Pressing `[Enter]` selects the option in brackets `[]`.

``` console
$ invenio-cli init --flavour=RDM
Initializing RDM application...
project_name [My Site]: February Release
project_shortname [february-release]:
project_site [february-release.com]:
github_repo [february-release/february-release]:
description [Invenio RDM February Release Instance]:
author_name [CERN]:
author_email [info@february-release.com]:
year [2020]:
Select database:
1 - postgresql
2 - mysql
3 - sqlite
Choose from 1, 2, 3 (1, 2, 3) [1]:
Select elasticsearch:
1 - 7
2 - 6
Choose from 1, 2 (1, 2) [1]:
-------------------------------------------------------------------------------

Generating SSL certificate and private key for testing....
Can't load /home/youruser/.rnd into RNG
139989104693696:error:2406F079:random number generator:RAND_load_file:Cannot open file:../crypto/rand/randfile.c:88:Filename=/home/youruser/.rnd
Generating a RSA private key
..................++++
..................................++++
writing new private key to 'docker/nginx/test.key'
-----
-------------------------------------------------------------------------------
Creating logs directory...
```

Observe the generated files. A full description of each of them can be found in the [invenio-cli RFC](https://github.com/inveniosoftware/rfcs/pull/4)

``` console
$ ls -la february-release
total 56
drwxr-xr-x 5 youruser youruser 4096 Feb 19 13:45 ./
drwxr-xr-x 5 youruser youruser 4096 Feb 19 13:45 ../
drwxr-xr-x 4 youruser youruser 4096 Feb 19 13:45 docker/
-rw-r--r-- 1 youruser youruser 2932 Feb 19 13:45 docker-compose.full.yml
-rw-r--r-- 1 youruser youruser  943 Feb 19 13:45 docker-compose.yml
-rw-r--r-- 1 youruser youruser 1152 Feb 19 13:45 Dockerfile
-rw-r--r-- 1 youruser youruser 2665 Feb 19 13:45 docker-services.yml
-rw-r--r-- 1 youruser youruser 2018 Feb 19 13:45 .invenio
-rw-r--r-- 1 youruser youruser 1504 Feb 19 13:45 invenio.cfg
drwxr-xr-x 2 youruser youruser 4096 Feb 19 13:45 logs/
-rw-r--r-- 1 youruser youruser  431 Feb 19 13:45 Pipfile
-rw-r--r-- 1 youruser youruser  756 Feb 19 13:45 README.rst
drwxr-xr-x 3 youruser youruser 4096 Feb 19 13:45 static/
```

**Notes and Known Issues**

- For now, the only available flavour is RDM (Research Data Management). In the future, there will be others, for example ILS (Integrated Library System).

- You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:`. Press `[Enter]` in that case. This will download the latest cookiecutter template.

- Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.


## Containerize and run your instance

The project is initialized, we just need to run it. Switch to the project
directory and do so:

``` console
$ cd february-release
$ invenio-cli containerize
<... build output ignored ...>
Instance running!
Visit https://localhost
$ firefox https://localhost
```

That is literally it! You now have a running instance of InvenioRDM at
https://localhost . You can get a sense for what InvenioRDM offers and explore.


## Conclusions

In just two commands you can get a preview of InvenioRDM:

``` console
$ invenio-cli init --flavour=RDM
$ cd <project name>
$ invenio-cli containerize
<... build output ignored ...>
Instance running!
Visit https://localhost
$ firefox https://localhost
```

These instructions don't provide you with a nice development experience though.
You need to run `invenio-cli containerize` for every change you make in your
project. That's slow and cumbersome. Up next, we show how to develop your
local instance and set yourself up to be productive!
