# Getting Started

You are now ready to learn how to create, customize and iterate on your own
InvenioRDM instance. In fact, the previous section showed you the last step before
deploying. You wouldn't want to fully containerize your application in the day
to day of developing your instance.

When working on your InvenioRDM application, you will want to use the commands
and the workflow we explain in these pages.

## Initialize your file system

We start by creating a new project in a different folder. We will just follow what we
did in the [Preview section](../preview/index.md). Feel free to use your own
project name.

``` bash
invenio-cli init --flavour=RDM
```
``` console
Initializing RDM application...
project_name [My Site]: Development Instance
project_shortname [development-instance]:
project_site [development-instance.com]:
github_repo [development-instance/development-instance]:
description [Invenio RDM Development Instance Instance]:
author_name [CERN]:
author_email [info@development-instance.com]:
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
Select file_storage:
1 - local
2 - S3
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


**Notes and Known Issues**

- For now, the only available flavour is RDM (Research Data Management). In the future, there will be others, for example ILS (Integrated Library System).

- You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:`. Press `[Enter]` in that case. This will download the latest cookiecutter template.

- Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.
