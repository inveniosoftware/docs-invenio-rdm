# Initialization

## Bootstrap your instance

### Initialize your file system

Running the `init` command and passing the requested configuration values will create the necessary files and folders in your working directory.

The CLI will require the following data:
- Project name: Title of your project with space allowed (project name for humans)
- Project short name: Hyphenated and lowercased title or one word (project name for machine)
- Project website: URL where the project will be deployed
- Github repository: Repository in format `<owner>/<code repository>`
- Description: Short description of project
- Author name: Your name or that of your organization
- Author email: Email for communication
- Year: The current year
- One of the three available storage systems: postgresql (default), mysql or sqlite
- The version of Elasticsearch: 7 (default) or 6

It will generate a test private key.

Enable your virtualenv or use `pipenv run` then run the `init` command. You will want to run all the commands from here on out in this virtualenv:

``` console
$ pipenv shell
(your-virtualenv)$ invenio-cli init --flavour=RDM
Initializing RDM application...
You've downloaded /home/youruser/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:
project_name [My Site]: December Release
project_shortname [december-release]:
project_site [december-release.com]:
github_repo [december-release/december-release]:
description [Invenio RDM December Release Instance]:
author_name [CERN]:
author_email [info@december-release.com]:
year [2019]:
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

Finally, observe the generated files. A full description of each of them can be found in the [invenio-cli RFC](https://github.com/inveniosoftware/rfcs/pull/4)

``` console
$ ls -la december-release
total 56
drwxr-xr-x 5 youruser youruser 4096 Dec 19 13:45 ./
drwxr-xr-x 5 youruser youruser 4096 Dec 19 13:45 ../
drwxr-xr-x 4 youruser youruser 4096 Dec 19 13:45 docker/
-rw-r--r-- 1 youruser youruser 2932 Dec 19 13:45 docker-compose.full.yml
-rw-r--r-- 1 youruser youruser  943 Dec 19 13:45 docker-compose.yml
-rw-r--r-- 1 youruser youruser 1152 Dec 19 13:45 Dockerfile
-rw-r--r-- 1 youruser youruser 2665 Dec 19 13:45 docker-services.yml
-rw-r--r-- 1 youruser youruser 2018 Dec 19 13:45 .invenio
-rw-r--r-- 1 youruser youruser 1504 Dec 19 13:45 invenio.cfg
drwxr-xr-x 2 youruser youruser 4096 Dec 19 13:45 logs/
-rw-r--r-- 1 youruser youruser  431 Dec 19 13:45 Pipfile
-rw-r--r-- 1 youruser youruser  756 Dec 19 13:45 README.rst
drwxr-xr-x 3 youruser youruser 4096 Dec 19 13:45 static/
```

**Notes and Known Issues**

For now, the only available flavour is RDM (Research Data Management). In the future, there will be others, for example ILS (Integrated Library System).

You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]: `. Type `yes` and press enter in that case. This will download the latest cookiecutter template.

Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.
