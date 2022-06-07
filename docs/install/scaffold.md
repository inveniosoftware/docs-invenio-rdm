# Scaffold

Now that you have Invenio-CLI [installed](cli.md), we will use it to scaffold a new instance of InvenioRDM.

## Initialize project

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
- **Python version**: 3.8 (default), 3.6, 3.7, or 3.9.
- **Database**: PostgreSQL (default) - we hope to support MySQL in the future.
- **Elasticsearch version**: 7 (default) or 6
- **Storage backend**: Local file system (default) or in a S3-like backend. If S3 is chosen a MinIO container is provided.

It will also generate a test private key which is needed for SSL support in the development server.

Let's do it! Pressing `[Enter]` selects the option in brackets `[]`.

``` bash
invenio-cli init rdm -c <version>
```

Where ``<version>`` should be replaced with he version you want to install, e.g.:

- LTS release (for production systems): ``v9.0``
- STS release (for feature previews): ``v9.0``

``` console
Initializing RDM application...
Running cookiecutter...
project_name [My Site]:
project_shortname [my-site]:
project_site [my-site.com]:
github_repo [my-site/my-site]:
description [My Site InvenioRDM Instance]:
author_name [CERN]:
author_email [info@my-site.com]:
year [2021]:
Select python_version:
1 - 3.8
2 - 3.7
3 - 3.6
4 - 3.9
Choose from 1, 2, 3, 4 [1]:
Select database:
1 - postgresql
Choose from 1, 2 [1]:
Select elasticsearch:
1 - 7
2 - 6
Choose from 1, 2 [1]:
Select file_storage:
1 - local
2 - S3
Choose from 1, 2 [1]:
Select development_tools:
1 - yes
2 - no
Choose from 1, 2 [1]:
-------------------------------------------------------------------------------

Generating SSL certificate and private key for testing....
Generating a 4096 bit RSA private key
...................................................................................................++
.............................................++
writing new private key to 'docker/nginx/test.key'
-----
-------------------------------------------------------------------------------
Writing invenio-invenio_cli config file...
Creating logs directory...
```

## Project structure

You can now inspect the generated project structure:

```
cd my-site
ls -a1
```

```console
.
..
.dockerignore
.gitignore
.invenio
.invenio.private
Dockerfile
Pipfile
README.md
app_data
assets
docker
docker-compose.full.yml
docker-compose.yml
docker-services.yml
invenio.cfg
logs
static
templates
```

Following is an overview of the generated files and folders:

| Name | Description |
|---|---|
| ``Dockerfile`` | Dockerfile used to build your application image. |
| ``Pipfile`` | Python requirements installed via [pipenv](https://pipenv.pypa.io) |
| ``Pipfile.lock`` | Locked requirements (generated on first install). |
| ``app_data`` | Application data for e.g. vocabularies. |
| ``assets`` | Web assets (CSS, JavaScript, LESS, JSX templates) used in the Webpack build. |
| ``docker`` | Example configuration for NGINX and uWSGI for running InvenioRDM. |
| ``docker-compose.full.yml`` | Example of a full infrastructure stack (DO NOT use in production!) |
| ``docker-compose.yml`` | Backend services needed for local development. |
| ``docker-services.yml`` | Common services for the Docker Compose files. |
| ``invenio.cfg`` | The Invenio application configuration. |
| ``logs`` | Log files. |
| ``static`` | Static files that need to be served as-is (e.g. images). |
| ``templates`` | Folder for your Jinja templates. |
| ``.invenio`` | Common file used by Invenio-CLI to be version controlled. |
| ``.invenio.private`` | Private file used by Invenio-CLI *not* to be version controlled. |

#### Notes and known issues

- You may be prompted with `You've downloaded /home/<username>/.cookiecutters/cookiecutter-invenio-rdm before. Is it okay to delete and re-download it? [yes]:`. Press `[Enter]` in that case. This will download the latest cookiecutter template.

- Some OpenSSL versions display an error message when obtaining random numbers, but this has no incidence (as far as we can tell) on functionality. We are investigating a possible solution to raise less eyebrows for appearance sake.
