# Runtime architecture

At its core InvenioRDM is an application built on-top of the Flask web
development framework, and fully understanding InvenioRDM's architectural design
requires you to understand core concepts of Flask which will be covered in brief here.

The Flask application is exposed via different *application interfaces*
depending on if the application is running in a web server, CLI or job queue.

InvenioRDM adds a powerful *application factory* on top of Flask, which takes
care of dynamically assembling an InvenioRDM application from the many individual
modules that make up InvenioRDM, and which also allows you to easily extend
it with your own modules.

## Core concepts

We will explain the core Flask concepts using a simple Flask application:

```python
from flask import Blueprint, Flask, request

# Blueprint
bp = Blueprint('bp', __name__)

@bp.route('/')
def my_user_agent():
    # Executing inside request context
    return request.headers['User-Agent']

# Extension
class MyExtension:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MYCONF', True)

# Application
app = Flask(__name__)
ext = MyExtension(app)
app.register_blueprint(bp)
```

You can save above code in a file ``app.py`` and run the application:

```console
$ pip install Flask
$ flask run
```

### Application and blueprint

InvenioRDM is a large application built up of many smaller individual modules. The
way Flask allows you to build modular applications is via *blueprints*.
In the above example, we have a small blueprint with just one *view*
(``my_user_agent``), which returns the browser's user agent sting.

This blueprint is *registered* on the *Flask application*. This allows you
to reuse the blueprint in another Flask application.

### Flask extensions

As blueprints allow you to modularise your Flask application's views,
Flask extensions allow you to modularise the initialization of your application
that is not specific to views (e.g. providing database connectivity).

A Flask extension is just an object like the one in the example above which has
an ``init_app`` method.

### Application and request context

Code in a Flask application can be executed in two "states":

- *Application context*: when the application is not handling requests e.g., in a CLI or running in a job queue
- *Request context*: when the application is handling a request from a user

In the above example, the  code inside the view ``my_user_agent`` is executed
during a request, and thus you can have access to the browser's user agent
string. On the other hand, if you tried to access ``request.headers`` outside
the view, the application would fail as no request is being processed.

The ``request`` object is a proxy object which points to the current request
being processed. There is some magic happening behind the scenes in order to
make this thread safe.

## Interfaces: WSGI, CLI and Celery

The Flask application runs via three different application
interfaces:

- **WSGI:** The frontend web server interfaces with Flask via Flask's WSGI
  application.
- **CLI:** The command-line interface is made using Click and takes care of
  executing commands inside the Flask application.
- **Celery:** The distributed job queue is made using Celery and takes care of
  executing jobs inside the Flask application.

## Application assembly

In each of the above interfaces, a Flask application needs to be created.
A common pattern for large Flask applications is to move the application
creation into a factory function, named an **application factory**.

InvenioRDM provides a powerful application factory for Flask which is capable of
dynamically assembling an application. In order to illustrate the basics of
what the InvenioRDM application factory does, have a look at the following
example:

```python
from flask import Flask, Blueprint

# Module 1
bp1 = Blueprint(__name__, 'bp1')
@bp1.route('/')
def hello():
    return 'Hello'

# Module 2
bp2 = Blueprint(__name__, 'bp2')
@bp2.route('/')
def world():
    return 'World'

# Application factory
def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp1)
    app.register_blueprint(bp2)
    return app
```

The example illustrates two blueprints, which are statically registered on the
Flask application blueprint inside the application factory. It is essentially
this part that the InvenioRDM application factory takes care of for you. InvenioRDM
will automatically discover all your installed InvenioRDM modules and register
them on your application.

### Assembly phases

The InvenioRDM application factory assembles your application in five phases:

1. **Application creation**: Besides creating the Flask application object,
   this phase will also ensure your instance folder exists, as well as route
   Python warnings through the Flask application logger.
2. **Configuration loading**: In this phase, your application will load your
   instance configuration. This essentially sets all the configuration
   variables for which you don't want to use the default values, e.g., the
   database host configuration.
3. **URL converter loading**: In this phase, the application will load any of
   your URL converters. This phase is usually only needed for some few specific
   cases.
4. **Flask extensions loading**: In this phase all the InvenioRDM modules which
   provide Flask extensions will initialize the extension. Usually the
   extensions will provide default configuration values they need, unless the
   user already set them.
5. **Blueprints loading**: After all extensions have been loaded, the factory
   will end with registering all the blueprints provided by the InvenioRDM modules
   on the application.
6. **URLs builder loading**: Now that the endpoints of the *current app* (UI or API) are loaded,
   the endpoints and associated URLs of the other app (respectively API or UI) are registered
   for the purpose of cross-app link generation.
7. **Final app loading**: After everythin else is loaded, the factory
   loads code dependent on having everything ready but the application not started.

Understanding the above application assembly phases, what they do, and how you
can plug into them is essential for fully mastering InvenioRDM development.

!!! note

    **No loading order within a phase**

    It's very important to know that, within each phase, there is **no order**
    in how the InvenioRDM modules are loaded. Say, within the Flask extensions
    loading phase, there's no way to specify that one extension has to be
    loaded before another extension.

    You only have the order of the phases to work with, so e.g., Flask extensions are
    loaded before any blueprints are loaded.

### Module discovery

In each of the application assembly phases, the InvenioRDM factory automatically
discovers your installed InvenioRDM modules. This works via Python
**entry point groups**. When you install the Python package for an InvenioRDM module,
the package describes via entry points which Flask extensions, blueprints etc.
it provides.

### WSGI: UI and REST

Each of the application interfaces (WSGI, CLI, Celery) may need slightly
different Flask applications. The InvenioRDM application factory is in charge
of assembling these applications, which is done through the above assembly
phases.

The WSGI application is however also split up into two Flask applications:

- **UI:** Flask application responsible for processing all user facing views.
- **API:** Flask application responsible for processing all REST API requests.

The reason to split the frontend part of InvenioRDM into two separate applications
is partly

- to be able to run the REST API on one domain (``api.example.org``) and the
  UI app on another domain (``www.example.org``)
- because UI and REST API applications usually have vastly different
  requirements.

As an example, a ``404 Not found`` HTTP error, usually needs to render a
template in the UI application, but returns a JSON response in the REST API
application.

### Implementation

The following InvenioRDM modules are each responsible for implementing parts of the
above application assembly, and it is highly advisable to dig deeper into
these modules for a better understanding of the InvenioRDM application
architecture:

- [InvenioRDM-Base](https://github.com/inveniosoftware/invenio-base): Implements the InvenioRDM
  application factory.
- [InvenioRDM-Config](https://github.com/inveniosoftware/invenio-config): Implements the
  configuration loading phase.
- [InvenioRDM-App](https://github.com/inveniosoftware/invenio-app): Implements default
  applications for WSGI, CLI and Celery.
