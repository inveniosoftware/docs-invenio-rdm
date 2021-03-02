# Architecture

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide provides a high-level architecture overview of the core part of InvenioRDM.

!!! warning "Work in progress"

    This section is under development.

## Layers

InvenioRDM has a layered architecture that consistent of three layers:

- Presentation layer
- Service layer
- Data access layer

There is a strict data flow between the layers, and each layer has very specific responsibilities. It's highly important that you as a developer know the basic principles for the  data flow and  each layer's responsibilities. Failure to understand the basic data flow, leads to using the wrong objects for the wrong things, which eventually turns into messy code.

### Data access layer

The data access layer is responsible for:

- Fetching and storing data on primary (the database) and secondary storage (Elasticsearch, cache, ...).
- Harmonizing data access to the same object on primary and secondary storages (e.g. a record in the database vs in the Elasticsearch index).
- Ensuring data integrity and managing relations among data objects.

The data access layer usually lives inside an Invenio module in a package named ``records``. It may consist of

- Record APIs (``/records/api.py``).
- JSONSchemas (``/records/jsonschemas/``).
- Elasticsearch mappings (``/records/mappings/``).
- SQLAlchemy models (``/records/models.py``).
- System fields (``/records/systemfields/``).
- Dumpers (``/records/dumpers/``).

**Principles**

TODO

- Data representation

- One primary storage, many secondary storages

- Data versioning

- Denormalize full objects

**Record API**

TODO

**JSONSchemas**

The JSONSchemas defines the structure of a JSON document we store in the database. The main responsibility is structural validation of the JSON document. The best analogy is that it is a database table schema. Most importantly, it is NOT responsible for business-level validation of the JSON document.

A good example of this, is making a field a required property. It's correct to require a property if you would e.g. have defined a database table column as ``NOT NULL``. It's wrong to require a property, if it's requirement that the user must enter a value in a certain field (because this is business-level validation, and you may want to store partially valid documents).

Modules:
- Invenio-Records: Defines the high-level APIs for the Record API, SQLAlchemy models, system fields and dumpers.
- Invenio-JSONSchemas: Provides a registry for JSONSchemas available to the application.

**Mappings**

The Elasticsearch mappings define how records are indexed and made searchable. Records are denormalised when indexed to provide high performance for searches over the records. The mapping MAY therefore define additional fields compared to the JSONSchema.

**Dumpers**

Dumpers are responsible for dumping and loading prior to storing/fetching records on secondary storage (e.g. the Elasticsearch index), and play a key role for harmonizing data access to records from primary and secondary storages.

Dumpers are specific to a secondary storage system (e.g. an Elasticsearch dumper, a file dumper, ...).

The dump and load of a dumper MUST be idempotent - i.e. ``record == Record.load(record.dump())``. This ensures that independently of if a record was retrieved from primary or secondary storage, it has the same data and works in the same manner.

For instance, the Extended Date Time Format dumper works in the following manner:

- The dump adds a start and end date range so that the EDTF can be queried by Elasticsearch.
- The load removes the two start and end date fields from the Elasticsearch document when loaded.

**System fields**

System fields are responsible for:

- providing *managed access* to a top-level property in a record
- manages relations with other objects
- hooking into the record life-cycle

System fields basically provides a programmatic API that makes it easier to work with records and related objects. Under the hood, system fields are Python data descriptors.

A key design principle for system fields, is that an *instance* of a system field manages a single namespace of a record so that system fields do not conflict. For instance an access system field manages the top-level ``access`` key in a record ``{'access': ...}``.

System fields participate in the dumping/loading of records from secondary storage via being able to hook into the record life-cycle. The difference between system fields and dumpers, is that a dumpers produce a dump fo a specific secondary storage system, while system fields produce the same dump for all secondary storage systems.

System fields may be used to manage relations to other objects, and can work similar to a foreign key.

Applications of system fields are vast, but some examples include:

- Added ``$schema`` to the record to ensure JSON schema validation.
- Created, update and delete persistent identifiers for records and serialize them into the record.
- Ensure a certain property on the JSON document is operated as a set.

System fields to a large degree avoids building inheritance among record APIs and instead provides a declarative way of composing a record API class.

**SQLAlchemy models**

SQLAlchemy record models are responsible for storing the master version of a record (i.e. the primary storage). All record models share some few common properties:

- A JSON column for storing the JSON-encoded document of a record.
- An internal UUID identifier.
- Creation and modification timestamps.
- Version counter for optimistic concurrency control.

UUIDs are used because they are storage efficient (128 bits) and random so that an application server can generate an id with low chance of collision.

It's important to understand that there's two distinct representations of a record:
- Python dictionary
- JSON document

These two distinct representations of a record may often be very similar, but it's important to understand that the JSON document is constrained to the JSON object model, while the Python dictionary can hold more rich types as long as they are JSON-serializable.

### Service Layer

The service layer contains the business logic of the application and is responsible for:

- Authorization (i.e. checking permissions)
- Business-level validation
- Control flow - e.g. transaction management,

**Principles**

TODO

- Mimick the end-user interface

- Independent of the Flask request context

 -Data flow

- Components responsible for setting data on a record.

- Who creates a service

**Service**

TODO

**Service config**

TODO

Responsibility:
- Inject dependencies via a single object.

**Service schema**

TODO

Responsibility:
- data validation
- field-level permission checking
- dumping and loading record projections


**Search**

TODO

Faceting, query parsing, etc.

**Permissions**

TODO

- Policy
- Need generators

**Components**

TODO

Responsible for providing a specific feature in the service, and make the service customizable.

### Presentation Layer

The presentation layer

## Customizations
