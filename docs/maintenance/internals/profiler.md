# Profiler

Invenio App RDM includes a profiler for analyzing Python and SQL performance.

## Features

- Start/stop profiling sessions from a web UI
- Collects and stores function-level profiling using [pyinstrument](https://github.com/joerick/pyinstrument)
- Collects and stores SQL query profiling using [sqltap](https://github.com/vinsci/sqltap)
- Profiling data is saved per-session as SQLite files in the configured storage directory.
- Generated reports can be viewed (or downloaded) per request for both the Python (base) and SQL layers.

## Installation

The profiler's dependencies are included in the `profiler` extra of `invenio-app-rdm`:

```
pip install invenio-app-rdm[profiler]
```

Or, if you are using `setup.cfg`, ensure the following:

```ini
[options.extras_require]
profiler =
    pyinstrument>=5.0.0,<6
    sqltap>=0.3.11,<1.0.0
```

## Enabling the profiler

By default, the profiler is **disabled** in production. To enable it, add the following in your `invenio.cfg` or environment:

```python
APP_RDM_PROFILER_ENABLED = True
# Optionally restrict profiler to administrators only 
# See: APP_RDM_PROFILER_PERMISSION in Customization below
```

## Customization

You may customize profiler behavior by setting Flask config variables:

- `APP_RDM_PROFILER_ENABLED`: `True`/`False` - enable/disable profiler
- `APP_RDM_PROFILER_STORAGE`: Path object or string, directory for profiler DBs (default: `$INSTANCE_PATH/profiler`)
- `APP_RDM_PROFILER_ACTIVE_SESSION_LIFETIME`: `timedelta`, how long a session is valid for (default: 60 min)
- `APP_RDM_PROFILER_ACTIVE_SESSION_REFRESH`: `timedelta`, session activity refresh window (default: 30 min)
- `APP_RDM_PROFILER_IGNORED_ENDPOINTS`: List of endpoint regexes to ignore (default: `["static", r"profiler\..+"]`)
- `APP_RDM_PROFILER_PERMISSION`: Callable returning True if current user can access the profiler (default: administrators only)


## Usage

With the profiler enabled and required dependencies installed:

1. Visit: `/profiler/` (e.g. http://localhost:5000/profiler/)
2. Start a profiling session by clicking "Start session", choosing:
    - an ID for the session,
    - whether to enable Python profiling,
    - whether to enable SQL profiling.
3. Interact with your site as usual. The profiler will collect profile data for each request.
4. Return to `/profiler/` to view and manage the collected profiling sessions and their reports.
