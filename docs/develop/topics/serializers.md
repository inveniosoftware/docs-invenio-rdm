# Building a serializer

Serializers and deserializers are responsible for translating between InvenioRDM's internal data
representation and external data formats. We'll use the term **serializers** to mean
both serializers and deserializers. Serializers are part of the
presentation layer in our [software architecture](../architecture/software.md).

## Key principles

A serializer should adhere to some few key principles. First and foremost, you
should think of a serializer as a translator. This means that the serializer
should be provided with all data it needs in order to perform the translation.
The sole purpose is to translate between formats. A serializer should for instance
**NOT**:

- handle HTTP requests and parse request parameters
- query the database or search index for extra information
- do business-level data validation

In addition, while you'll most often use serializers to provide new formats
on the REST API, it's important to understand that serializers can also be used
as part of the backend when e.g. writing archival packages to disk.

You can thus think of serializer as translators from/to a stream of bytes:

- Deserialize: Decode a stream of bytes to our internal data representation
- Serialize: Encode our internal data representation as a stream of bytes.

![High-level view of serializers and deserializers.](../img/serializer.svg)

## Use case

The following use case will focus on how to build a serializer and configure it
on the REST API and use it as content negotiation. As mention above, this is
the most common use case, but not the only one.

In the following we'll build a very basic JSON serializer. Note, that this
already exists, so it only serves as an example showing how it works.

## Directory structure

We include the serializer as part of the presentation layer, so often you'll
find it in the ``resources`` folder.

```
|-- resources
    |-- __init__.py
    |-- config.py
    |-- resources.py
    |-- deserializers
    |   |-- __init__.py
    |   `-- json/
    |       |-- __init__.py
    |       `-- ...
    `-- serializers
        |-- __init__.py
        `-- json/
            |-- __init__.py
            `-- schema.py
```

We often put a serializer in its own Python package (the ``json`` folder) as it
may often have mulitple files. If there's only a single file, you can replace
the folder with a Python module instead (e.g. ``json.py``).

## Configuring the REST API

This guide does not cover how you use the serializer in the REST API. Please
see how to do this in the [building resources](resource.md#response-serialization-content-negotiation)
under "Response serialization (content negotiation)".

## Serializer

A serializer implements a simple interface defined in the
[Flask-Resources](https://github.com/inveniosoftware/flask-resources) package:

```python
# serializers/json/__init__.py
import json
from flask_resources.serializers import SerializerMixin

class JSONSerializer(SerializerMixin):

    def serialize_object(self, obj):
        """Dump the object list into a JSON UTF-8 encoded byte string"""
        # The obj is Python dict representation
        return json.dumps(obj)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON UTF-8 encoded byte string."""
        # The obj_list is a list of Python dict representations
        return json.dumps(obj_list)
```

Notes:

- ``serialize_object()`` takes a Python dict representation and dumps it to
  JSON.
- ``serialize_object_list()`` takes a list of Python dict representation and
  dumps it to JSON.

The two methods are separated as often the list version requires wrapping an
envelope around the objects. Note that it's not required to implement both
methods.

## Deserializer

A deserializer is similar to a serializer:

```python
# deserializers/json/__init__.py
import json
from flask_resources.deserializers import DeserializerMixin

class JSONDeserializer(SerializerMixin):

    def deserialize(self, data):
        """Deserializes the byte stream into an Python dictionary."""
        return json.loads(data)
```


## Data transformations

The serializer doesn't require you to use any specific method for the
implementing them as long as they adhere to the API interface. However, often
you're faced with some sort of data transformations, and for this InvenioRDM
normally uses the [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
library as a declarative way of specifying this transformation.

First, you'll create a schema:

```python
# serializers/json/schema.py

from marshmallow import Schema, fields

class MySchema(Schema):
    title = SanitizedUnicode(attribute="metadata.title")
    # ...
```

Above simple schema for instance can translate a Python dictionary from:

```python
{"metadata": {"title": "Test", "akey": "avalue"}}
```

to (moving ``title`` to a top-level key and stripping ``akey``):

```python
{"title": "Test"}
```

## Using schemas

The schema can then be combined with the Marshmallow serializer, it takes three arguments:

- format_serializer_cls: class in charge of transforming the data object into the desired
format. In the example below the output is formatted as JSON but it could be any other
(e.g. XML).
- object_schema_cls: Marshmallow Schema of the object.
- list_schema_cls: Marshmallow Schema of the object list.


```python
# serializers/json/__init__.py

from flask_resources import MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

from .schema import MySchema

class MySerializer(MarshmallowSerializer):
    def __init__(self, **options):
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=MySchema,
            **options  # passed as context to the Marshmallow schema
        )
```

Then you can add it to the list of response handlers that are accepted by the API:

```python
# resources/config.py
from .serializers import MySerializer

class ClickResourceConfig(ResourceConfig):
    response_handlers = {
        "application/json": ResponseHandler(MySerializer())
    }
```

## Advanced serialization

The serialization and deserialization can be become pretty complex, and often
there might be existing tools you may want to leverage for more complex data
models. Before writing your own serializer, we encourage you to explore the
serializers in [Invenio-RDM-Records](https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/resources/serializers)
for more advanced use cases.

You'll find examples of schemas, XML serializers, pipelines (such as Python
dictionary -> DataCite JSON -> DataCite XML).

- Dictionary to MARC21 representation using dojson
- MARC21 representation to MARCXML
- MARCXML to MODS using XSLT.
