# Building a service

The service layer is a high-level entry point into your application. Often, you'll have a direct connection between e.g. a button in the UI and a single service method. The service layer contains the domain and business logic of the application and is e.g. responsible for checking permissions, business-level validation and overall control flow.

## Designing a service

Before you start writing your service, it's highly important you spend time on
designing your service first. Clearly

- Define responsibilities
- Define names

As a service often defines transactional boundaries in your code, this often
implies that the domain objects will have a rather tight coupling.

## Directory structure

A service is normally split over multiple files. Below is an example of such a
module structure:

```
|-- __init__.py
|-- components/
|   |-- __init__.py
|   `-- <component>.py
|-- config.py
|-- customizations.py
|-- errors.py
|-- permissions.py
|-- result_items.py
|-- schema.py
`-- service.py
```

## Service

A service in itself is quite basic. For instance, we can imagine building a
click service with a single service method.

```python
# service.py
from invenio_records_resources.services import Service

class ClickService(Service):

    def click(self, identity):
        # do something ..
```

!!! tip

    The control flow of your service methods should be easy to follow and
    understand for your colleagues. If it's not, you are either missing new entities
    in the service layer or your data layer is not well-defined enough.


## Service config

Each service also always has a configuration which is used for dependency
injection:

```python
# config.py
from invenio_records_resources.services import ServiceConfig

class ClickServiceConfig(ServiceConfig):
    permission_policy_cls = ...
```

## Instantiating a service

Before you can use a service, the service always has to be instantiated:

```python
from flask import current_app
from invenio_access.permissions import system_identity

from .services import ClickService, ClickServiceConfig

service = ClickService(ClickServiceConfig.build(current_app))
service.click(system_identity)
```

This basically means that all dependencies that can be customized
are injected in the service via the config.

## Service results

A service is always independent of the presentation layer and thus all
parameters must be passed explicitly to a service. Furthermore, a service must do
all permission checking, thus a service usually never returns a data layer object
directly. Instead, it normally returns a view of a data layer object specific to a
given identity:

```python
# service.py
from invenio_records_resources.services import Service

class ClickService(Service):
    def click(self, identity):
        # Retrieving a data layer object
        record = ...

        # The data layer object is wrapped in a service result
        return self.result_item(
            self,
            identity,
            record,
            # ...
        )
```

The class used to wrap the record in the above case is set via the config:

```python
# config.py
from invenio_records_resources.services import ServiceConfig

from .result_items import RecordView

class ClickServiceConfig(ServiceConfig):
    result_item_cls = RecordView
```

The result item itself, often provides a ``to_dict()`` method that's used by
the presentation layer:

```python
# result_items.py
from invenio_records_resources.services.base import \
    ServiceItemResult

class RecordView(ServiceResultItem):
    def __init__(self, identity, record):
        self._identity = identity
        self._record = record

    def to_dict(self):
        # .. view of the record for the given identity ...
```

## Errors

An important aspect of a service is that in case of errors it should always
raise a domain error. These errors should be well-defined so that the presentation
layer can respond with a correct message.

Always define a base class for errors, and the individual errors:

```python
# errors.py
class ClickException(Exception):
    pass

class AlreadyClickedError(ClickException)
    # ...
    pass
```

A service method can then raise the error:

```python
# service.py
from invenio_records_resources.services import Service

from .errors import AlreadyClickedError

class ClickService(Service):
    def click(self, identity):
        # ...
        raise AlreadyClickedError()
```

!!! info

    You should never raise an ``HTTPException`` from a service method or use the
    Flask ``abort(404)`` method.

## Permissions

#### Checking permissions

A service method nearly always checks permissions first thing:

```python
# service.py
from invenio_records_resources.services import Service

class ClickService(Service):
    def click(self, identity):
        # the "click" maps to "can_click" in the permission policy
        self.require_permission("click", identity, ...)
```

The identity must always be given explicitly to the service methods. Thus, often
in the REST API (presentation layer), you'll see the identity passed in like
below:

```python
from flask import g

def view()
    service.click(g.identity)
```

#### Defining permission policies

The ``require_permission()`` method delegates permission checks to a permission
policy for the given service. The policy is defined in the config:

```python
# config.py
from invenio_records_resources.services import ServiceConfig

from .permissions import ClickPermissionPolicy

class ClickServiceConfig(ServiceConfig):
    permission_policy_cls = ClickPermissionPolicy
```

The permission policy itself is defined in a declarative way:

```python
# permissions.py
from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess

class ClickPermissionPolicy(RecordPermissionPolicy):
    can_click = [AnyUser(), SystemProcess()]
```

The ``AnyUser()`` and ``SystemProcess()`` objects are called "need generators".

## Service components

Services usually define many methods that each may be dealing with multiple
independent concerns. For instance the ``create()`` method may need to set
metadata on a data layer object as well as register a persistent identifier,
while the ``delete()`` method may need to just delete the persistent identifier.

A service component groups related functionality across service
methods, so for instance a ``PIDComponent`` would implement the ``create()``
and ``delete()`` method related to registering/deleting a persistent identifier
while a ``Metadata`` component would only deal with metadata in its service
methods.

```python
# service.py
from invenio_records_resources.services import Service

class ClickService(Service):
    def click(self, identity):
        # ...
        self.run_components(
            'click', # name identical to method's.
            identity, # arguments identical to the method's.
        )

        return self.result_item(...)
```

The components are injected in the service config:

```python
# config.py
from invenio_records_resources.services import ServiceConfig

from .components import MetadataComponent

class ClickServiceConfig(ServiceConfig):
    components = [
        MetadataComponent,
    ]
```

The components themselves:

```python
# components.py
from invenio_records_resources.services import ServiceComponent

class MetadataComponent(ServiceComponent):
    def click(self, identity, **kwargs):
        # ...
```

!!! note

    Service components are not mandatory to use, but they help keep service methods
    clean and readable by separating independent concerns.

## Unit of work

Any state-changing service methods (i.e. create, delete, ...) must support the
unit of work pattern to allow grouping multiple service methods into a single
atomic operation.

In a service method, you should never use ``db.session.commit()``, but
instead use the `unit_of_work()` decorator like below:

```python
from invenio_records_resources.services import Service
from invenio_records_resources.services.uow import unit_of_work, RecordCommitOp

class ClickService(Service):

    @unit_of_work()
    def click(self, ..., uow=None):
        record = ...
        # Register an operation on the unit of work.
        uow.register(RecordCommitOp(record, indexer=self.indexer))
        return ...
```

## Bootstrapping a service

Once you've written a service, you'll need to create an instance of the service
to be used in the Flask application. The overall pattern you'll often see used
is that the resources and services are created as below in `ext.py`:

```python
# ext.py
from .services import ClickService, ClickServiceConfig

class MyExtension:
    # ...
    def init_app(self, app):
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)

    def init_config(self, app):
        # ....

    def init_services(self, app):
        # Prepare all service configs
        configs = self.service_configs(app)
        # Set the services
        self.service = ClickService(configs.click_service)

    def service_configs(self, app):

        class Configs:
            click_service = ClickServiceConfig.build(app)
            # other service configs could be defined here

        return Configs
```

In addition, a proxy is set up to access the current service:

```python
# proxies.py
from flask import current_app
from werkzeug.local import LocalProxy

current_myextension = LocalProxy(
    lambda: current_app.extensions['myextension']
)

current_clickservice = LocalProxy(
    lambda: current_myextension.service
)
```
