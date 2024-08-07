# Names

Names are a specific type of vocabulary, which represent a records' creator
or contributor. For example, the deposit form offers _search as you type_
suggestions and auto-fills the corresponding information.

You can find information behind the design and usage of the vocabulary in
[RFC 0054](https://github.com/inveniosoftware/rfcs/pull/54).

## Data model

A _Name_ record contains:

- The name of the author split in `family name` and `given name`, or a
  single `name` attribute with the full name formatted as
  `<family name>, <given name>`. Note that if `family name` and `given name`
  are present they will overwrite `name`.
- A list of `identifiers`, composed by their identifier value and scheme.
  The scheme can potentially be autocompleted if it is known by the _idutils_
  library (e.g. ORCID).
- A list of `affiliations`, which can be represented by its `name` or, if it
  belongs to the _Affiliations_ vocabulary, by its `id`.

```yaml
- family_name: Carberry
  given_name: Josiah
  id: 0000-0002-1825-0097
  identifiers:
    - identifier: https://orcid.org/0000-0002-1825-0097
      scheme: orcid
  affiliations:
    - name: Wesleyan University
- name: Haak, Laurel L
  id: 0000-0001-5109-3700
  identifiers:
    - identifier: https://orcid.org/0000-0001-5109-3700
  affiliations:
    - id: 04fa4r544
```

### How to import and update your name records

InvenioRDM ships with an example set of names and ORCID identifiers.
To disable these from being loaded, create a blank file called
`app_data/vocabularies/names_orcid.yaml`.

The Names vocabulary uses the new DataStreams API for processing vocabularies.
You can find more information about this new API in
[RFC 0053](https://github.com/inveniosoftware/rfcs/pull/53).

!!! warning "Use of the `vocabularies` command"
    Name records will not be managed by the usual
    `invenio rdm-records fixtures` command, but instead
    a set of `invenio vocabularies ...` commands.

There are several ways to import names records. The most straight forward
is by a DataStream definition file, where you will define how entries from a
data source will be **read**, if they need any **transformation**, and finally
where they should be **written** to.

For a simple import you can **read** entries from a YAML file with raw metadata
objects, skip **transformations**, and use a service API to **write** and
persist the entries to the database. Here is an example of this definition
file, lets call it `vocabularies-future.yaml`:

```yaml
names:
  readers:
    - type: yaml
      args:
        origin: "./app_data/names.yaml"
  writers:
    - type: names-service
      args:
        update: false
```

Finally, to run an **import** using this `vocabularies-future.yaml` file you
can call the `vocabularies import` command:

```shell
invenio vocabularies import \
  --vocabulary names \
  --filepath ./vocabularies-future.yaml
```

In addition, you can also **update** vocabulary records in case you updated the
source data file using the `vocabularies update` command:

```bash
invenio vocabularies update \
  --vocabulary names \
  --filepath ./vocabularies-future.yaml
```

### Creating a `names.yaml` file

The Names vocabulary has been implemented with the
[ORCID public dataset](https://support.orcid.org/hc/en-us/articles/360006897394-How-do-I-get-the-public-data-file)
as a possible source to import entries from. This means that the functionality
to **read** entries from this format is already available. For example, you
can use the `vocabularies convert` command to convert this dataset into a YAML
file with the appropriate names metadata format:

```bash
invenio vocabularies convert \
  --vocabulary names \
  --origin /path/to/ORCID_2021_10_summaries.tar.gz \
  --target names.yaml
```

Alternatively, you can simply import it directly:

!!! warning "Long and blocking operation"
    Note that the import process is done synchronously and the ORCID dataset is
    very large. Therefore, this operation can take a long time.

```bash
invenio vocabularies import \
  --vocabulary names \
  --origin /path/to/ORCID_2021_10_summaries.tar.gz
```

### Using ORCiD Public Data Sync

#### Installing Required Dependencies

First, you should install the required `s3fs` dependency. This can be achieved by adding the following to the `Pipfile` in your instance:

```toml
[packages]
...
invenio-vocabularies = {extras = ["s3fs"]}
...
```

#### Configuring ORCiD Public Data Sync

InvenioRDM supports loading names using the ORCiD Public Data Sync. To set this up, you need to create a definition file named `names-orcid.yaml` with the following content:

```yaml
names:
  readers:
    - type: orcid-data-sync
    - type: xml
  transformers:
    - type: orcid
  writers:
    - type: async
      args:
        writer:
          type: names-service
  batch_size: 1000
  write_many: true
```

#### Customizing the Sync Interval

Optionally, you can specify the sync interval for the orcid-data-sync reader by adding arguments. If not specified, the default sync interval is one day. The supported arguments for defining the interval are:

	•	years
	•	months
	•	weeks
	•	days
	•	hours
	•	minutes
	•	seconds
	•	microseconds

Here is an example of how to set a custom sync interval of 10 days:

```yaml
names:
  readers:
    - type: orcid-data-sync
      args:
        since: 
          days: 10
    - type: xml
  transformers:
    - type: orcid
  writers:
    - type: async
      args:
        writer:
          type: names-service
  batch_size: 1000
  write_many: true
```
#### Running the Import Command

To run an import using the names-orcid.yaml file, use the vocabularies import command as shown below:

```shell
invenio vocabularies import \
  --vocabulary names \
  --filepath ./names-orcid.yaml
```
