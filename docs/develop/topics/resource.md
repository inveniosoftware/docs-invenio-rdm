# Building a resource

A resource belongs to the presentation layer and is used to build REST APIs. A
resource is at the core essentially a Flask Blueprint.

## Directory structure

A resource normally split over multiple files. Below is an example of such a
module structure:

```
|-- __init__.py
|-- config.py
`-- resource.py
```

## Resource

A basic resource is created from the Flask-Resources library, and one or more
service is injected in addition to a resource config:

```python
# resource.py
from flask import g
from flask_resources import Resource

class ClickResource(Resource):
    def __init__(self, config, service):
        super().__init__(config)
        self.service = service
```

## Resource config

The resource config is used for dependency injection in the resource. The
basics is e.g. that we allow modifying the routing for the REST API (i.e.
routing is independent of implementation):

```python
# config.py
class ClickResourceConfig(ResourceConfig):
    # Blueprint configuration
    blueprint_name = "click"
    url_prefix = "/click"
    routes = {
        "click": "/", # relative to url_prefix
    }
    # ...
```

## Instantiating a resource

A resource needs to be instantiated first and registered on a Flask
application:

```python
service = ...
resource = ClickResource(ClickResourceConfig(), service)

# Register the resource as a blueprint on the Flask application.
app = Flask()
app.register_blueprint(resource.as_blueprint())
```

## Routing

A resource must implement the ``create_url_rules()`` method to define the
view routing:

```python
# resource.py
from flask_resources import route

class ClickResource(Resource):
    def create_url_rules(self):
        # Get the named routes from the config
        routes = self.config.routes
        # Define the URL rules:
        return [
            route("POST", routes["click"], self.click),
        ]

    def click(self):
        # ... view implementation ...
```

## Response serialization (content negotiation)

Content negotiation allows to support multiple different metadata formats on
the same endpoint, which can also be used for versioning the REST API.

Below is an example of how the result item from the service, is return
as a dict to the response handler:

```python
# resource.py
from flask_resources import response_handler

class ClickResource(Resource):
    # Decorate the view
    @response_handler()
    def click(self):
        # Call service
        item = self.service.click(g.identity)
        # a Python dictionary is returned to the response handler which will
        # serialize it into the desired format.
        return item.to_dict(), 200  # HTTP 200 status code.
```

The actual serialization is defined by the config (e.g. we allow users to
overwrite the output of the REST API):

```python
# config.py
from flask_resources import response_handler

class ClickResourceConfig(ResourceConfig):
    response_handlers = {
        # Define JSON serializer for "application/json"
        "application/json": ResponseHandler(JSONSerializer())
    }
```

The ``JSONSerializer`` is responsible for turning the Python dictionary (from
``item.to_dict()``) into byte string, and the ``ResponseHandler`` is responsible
for wrappging the byte string in an HTTP response.

## Parameter parsing

#### Resource request context

A view method in a resource should parse all its parameters and store them
on the resource request context. This way we ensure all input data have passed
some basic validation.

#### Parsing the URL query string

Below is an example of parsing a required URL query string parameter ``q`` (
e.g. ``/click?q=...``):

```python
# resource.py
class ClickResource(Resource):
    @request_parser(
        {'q': ma.fields.String(required=True)},
        # Other locations include args, view_args, headers.
        location='args',
    )
    @response_handler()
    def click(self):
        # The validated data is now available on the resource request context:
        resource_requestctx.args['q']
```

#### Parsing the request body

The HTTP request body can be parsed as well:

```python
class ClickResource(Resource):
    @request_body(
        parsers={
            "application/json": RequestBodyParser(JSONDeserializer())
        }
    )
    @response_handler()
    def click(self):
        # The validated data is now available on the resource request context:
        resource_requestctx.data
```

## Error handling

The resource further allows you to easily map service layer errors to an HTTP
error. Below is an example of mapping the `` AlreadyClickedError to an
``400`` Bad Request HTTP error:

```python
# resource.py
from flask_resources import Resource, HTTPJSONException, create_error_handler
from ..service.errors import AlreadClickedError

class ClickResource(Resource):
    # Set the error handlers to map service errors to HTTP errors.
    error_handlers = {
        AlreadyClickedError: create_error_handler(
            HTTPJSONException(
                code=400,
                description="Already clicked.",
            )
        )
    }
```

## Bootstrap

