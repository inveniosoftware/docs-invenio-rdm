# Upgrading from v3.0 to v4.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 3.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.


## Upgrade Steps

This release includes some changes in IIIF packages, which require the [ImageMagick](https://imagemagick.org/script/download.php) binaries. These binaries have been added the the base image of inveniosoftware. Therefore, make sure you use the latest base image or you install those binaries. To use the latest base image you just need to pull from dockerhub:

```
docker pull inveniosoftware/centos7-python:3.6
docker pull inveniosoftware/centos8-python:3.7
docker pull inveniosoftware/centos8-python:3.8
```

First, latest `invenio-cli` must be installed. After, the Elasticsearch indices are deleted and the packages are upgraded. Following this step, you can optionally prepare your custom fixtures. Then, the upgrade command will be executed. This will migrate the database, run the custom migration script and rebuild the Elasticsearch indices.

This can be achieved by the following Bash shell commands:

~~~bash
# NOTE: make sure you're in the instance directory

# Upgrade invenio-cli
pip install invenio-cli --upgrade

# Delete ES indices
pipenv run invenio index destroy --yes-i-know

# Upgraded packages
sed -i -E '/invenio = "~=3.4.0"/d' Pipfile
invenio-cli packages update 4.0.1
invenio-cli assets build -d
~~~

We need the server running in another terminal for the next steps, in a new console run:

~~~bash
# NOTE: make sure you're in the instance directory

invenio-cli run
~~~

Now, when the server is started, in the previous console you can optionally [prepare your fixtures](../../customize/vocabularies/index.md):

~~~bash
# NOTE: make sure you're in the instance directory

# If you relied on resource_types.csv in your app_data/ folder, you will want to convert them first
cp $(find $(pipenv --venv)/lib/*/site-packages/invenio_rdm_records -name convert_to_new_vocabulary.py) .
pipenv run python convert_to_new_vocabulary.py app_data/vocabularies/resource_types.csv --to app_data/vocabularies/
# this should create app_data/vocabularies/resource_types.yaml

# Add vocabularies.yaml file to tell RDM to use this vocabulary
 echo "resource_types:
    pid-type: rsrct
    data-file: vocabularies/resource_types.yaml
  " > app_data/vocabularies.yaml
# if you want to add users follow instructions at the link above.
~~~

Finally, whether you added custom fixtures or not, you need to at least load the defaults ones and upgrade existing records:
~~~bash
# Do the migration
pipenv run invenio rdm-records fixtures
invenio-cli upgrade --script $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_3_0_to_4_0.py)
~~~
