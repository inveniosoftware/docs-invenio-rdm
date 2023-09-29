# Migrate legacy routes

*Introduced in InvenioRDM v11*

This guide describes the process to migrate legacy routes using the redirector module.

## Redirector module

The redirector module registers legacy routes (called **source**) and the redirection to a new **target**.

Redirection rules are retrieved by the application from the config `REDIRECTOR_RULES`.

## Steps

- Identify the old endpoint url (e.g. `/old_endpoint`)
- Identify the new endpoint url (e.g. where to redirect a request to `/old_endpoint`).
- Add the config `REDIRECTOR_RULES` in the application (e.g. `my_syte/config.py`). E.g:
  ```python
    REDIRECTOR_RULES = {
        "redirect_my_rule": {
            "source": "/old_endpoint",
            "target": "/new_endpoint"
        }
    }
  ```

## Examples

Sometimes it is necessary to modify the request further (e.g. map old parameters to newer ones). The redirector module also accepts a function that returns a URL as the rule's `target`.
Find below some examples

- Redirect a request to a new endpoint.

```python
REDIRECTOR_RULES = {
  "redirect_my_rule": {
      "source": "/old_endpoint",
      "target": "/new_endpoint"
  }
}
```

- Redirect a request to a new endpoint whose view arguments have changed.

```python
def redirect_function():
    # Anything is allowed here, as long as the function returns a valid url.
    from flask import url_for
    values = request.view_args
    # A new argument is injected
    values["new_argument"] = "foo"
    target = url_for("new_endpoint", **values)
    return target

REDIRECTOR_RULES = {
    "redirect_rule": {
        "source": "/old_endpoint",
        "target": redirect_function
    }
}
```

- Redirect a request to a new endpoint, specifying an HTTP code for the redirection.

```python
def redirect_function():
    # Anything is allowed here, as long as the function returns a valid url.
    from flask import url_for
    values = request.view_args
    # A new argument is injected
    values["new_argument"] = "foo"
    target = url_for("new_endpoint", **values)
    return target, 302

REDIRECTOR_RULES = {
    "redirect_rule": {
        "source": "/old_endpoint",
        "target": redirect_function
    }
}
```
