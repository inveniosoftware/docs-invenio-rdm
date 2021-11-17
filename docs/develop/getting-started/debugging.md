# Debugging

**Python debugger**

For debugging use the Python debugger (PDB) or one of the variations (ipdb, pytest and wdb).

To set a breakpoint place the following code:

```python
breakpoint()
```

**Flask DebugToolbar**

You can also install [Flask-DebugToolbar](https://flask-debugtoolbar.readthedocs.io/en/latest/):

```
cd ~/src/my-site
pipenv run pip install Flask-Debugtoolbar
```

It has built-in:

- Profiler
- SQL queries logging
- View config/templates

**SQL queries**

Last, but not least you can print SQL queries to the console by setting the  variable in your ``config.py``:

```
# config.py
SQLALCHEMY_ECHO = True
```
