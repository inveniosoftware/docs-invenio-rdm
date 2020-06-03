# Getting Started

You are now ready to learn how to create, customize and iterate on your own
InvenioRDM instance. In fact, the previous section showed you the last step before
deploying. You wouldn't want to fully containerize your application in the day
to day of developing your instance.

When working on your InvenioRDM application, you will want to use the commands
and the workflow we explain in these pages.

## Initialize your file system

We start by creating a new project in a different folder. We will follow what we
did in the [Preview section](../preview/index.md). Feel free to use your own
project name.

!!! warning "New pre-requisite: set FLASK_ENV=development"
    To be able to modify assets and work on dependent modules, the environment variable
    `FLASK_ENV` must be set to `development` in your shell for all subsequent operations.
    This was not needed when running `invenio-cli containerize` since everything runs in
    containers and you are not developing. We show how to do so below, but you can also
    consult the [development setup page](https://github.com/inveniosoftware/invenio-app-rdm/wiki/Development-Setup)
    for more up-to-date and advanced information.

We need to set the `FLASK_ENV` environment variable. Make sure you do so in each terminal you are
running `invenio-cli` commands from now on.

With the bash shell:

``` bash
export FLASK_ENV=development
```

With the fish shell:

```fish
set --export FLASK_ENV development
```

Then we can run the initialization command:

``` bash
invenio-cli init rdm
```
``` console
Initializing RDM application...
Running cookiecutter...
project_name [My Site]: Development Instance
project_shortname [development-instance]:
project_site [development-instance.com]:
github_repo [development-instance/development-instance]:
description [Invenio RDM Development Instance Instance]:
author_name [CERN]:
author_email [info@development-instance.com]:
year [2020]:
Select python_version:
1 - 3.6
2 - 3.7 (development only)
3 - 3.8 (untested)
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


**Notes and Known Issues**

- For now, the only available flavour is RDM (Research Data Management). In the future, there will be others, for example ILS (Integrated Library System).

- You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:`. Press `[Enter]` in that case. This will download the latest cookiecutter template.

- Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.
