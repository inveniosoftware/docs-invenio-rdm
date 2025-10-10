## Overview

Migrating from Pipenv to [`uv`](https://docs.astral.sh/uv/) brings significantly faster
dependency resolution and better alignment with modern Python packaging standards using
`pyproject.toml`.

### Install `uv`

Before starting with any migration steps, [install
uv](https://docs.astral.sh/uv/getting-started/installation/) on your system. It's
recommended to use the standalone installer, since it's independent of any system
package managers (like `apt` or `brew`) and the installed binary comes with a
self-upgrading mechanism using `uv self upgrade`.

On top of this it's recommended that you start using `uv` to manage the `invenio-cli` tool
installation. Make sure you uninstall any existing `invenio-cli` installation first, and
then run `uv tool install invenio-cli`.

## Migration script

To ease the migration process, a [helper Python script](./uv_migrate.py) is available
for automating the following steps of this guide:

- Converting your `Pipfile` to a `pyproject.toml` file
- Updating your `site/` package configuration to use `pyproject.toml`
- Updating your `.invenio` configuration to use `uv`
- Removing old unnecessary files (`Pipfile`, `Pipfile.lock`, `setup.cfg`, `MANIFEST.in`, etc.)

The script assumes a "standard" InvenioRDM bootstrapped project structure (e.g. it reads
from the `.invenio` file to auto-detect the project name, Python version, and author
info), so you may come across issues if your project structure and configuration has
deviated significantly. In any case, the script is just a starting point, and you will
still need to manually verify and adjust the following:

- your `Dockerfile` (if you rely on Docker for application development or deployment)
- your tests suite
- CI/CD configuration (e.g. if you're using GitHub Actions)
- any other custom scripts that use Pipenv

This guide covers the most common aspects, but as with any migration, testing of the
final result is crucial. Make sure you run your application and try all the development
and operational workflows that you would normally use.

To run the script follow these steps:

```bash
# Navigate to your InvenioRDM instance directory
cd my-site/

# Download the script in a temporary location
curl -LsSf https://raw.githubusercontent.com/inveniosoftware/docs-invenio-rdm/main/docs/releases/uv_migrate.py -o /tmp/uv_migrate.py

# Run the script using uv
uv run /tmp/uv_migrate.py
```

## Step-by-Step Migration Guide

!!! note "Steps covered by the script"
    Steps that the `uv_migrate.py` script covers are marked with a 📜 icon in their header.

### Convert `Pipfile` to `pyproject.toml` 📜

Create a root `pyproject.toml` file to replace your `Pipfile` in the root of your
project. All dependencies, including test dependencies, are now managed in this single
file:

#### Before: `Pipfile`

```toml title="Pipfile"
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[packages]
invenio-app-rdm = {version = "~=13.0.0", extras = ["opensearch2"]}
my_site = {editable=true, path="./site"}
# ... other dependencies

[requires]
python_version = ">=3.12"
```

#### After: `pyproject.toml`

```toml title="pyproject.toml"
[project]
name = "my-site-app" # (1)!
version = "1.0.0" # (2)!
authors = [{ name = "My Organization" }] # (3)!
license = "MIT"
requires-python = ">=3.12"
dependencies = [
    "invenio-app-rdm[opensearch2]~=13.0.0",
    "my-site", # (4)!
    # ... other dependencies
]

[tool.uv.sources] # (5)!
my-site = { workspace = true }

[tool.uv.workspace] # (6)!
members = ["site"]

[dependency-groups] # (7)!
dev = [
    "pytest-invenio>=3.0.0,<4.0.0",
    # ... other dev dependencies
]
```

1. The project needs the `-app` suffix to avoid package naming conflicts between the root project and site package (see below)
2. Project version is now required in `pyproject.toml`
3. Project metadata like authors and license are now explicitly defined
4. References the workspace member defined in `[tool.uv.workspace]`
5. Defines where uv should find local packages (including workspace members)
6. Declares this is a workspace project with "site" as a member package
7. Replaces Pipfile's `[dev-packages]` - groups dependencies by their purpose

??? info "Understanding uv Workspaces"

    `uv` introduces the concept of
    [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) - a way to
    manage multiple related packages in a single repository. In InvenioRDM projects,
    your custom code in the `site/` directory becomes a workspace member, allowing uv
    to manage dependencies across multiple packages in a unified way at the root
    `pyproject.toml`.

### Update `site/pyproject.toml` 📜

Update your site-specific package configuration:

#### Before: `site/setup.cfg`

```ini title="site/setup.cfg"
[metadata]
name = my-site

[options.extras_require]
tests =
    pytest-invenio>=3.0.0,<4.0.0
    # ...other test dependencies

[options.entry_points]
invenio_base.blueprints =
    my_site_views = my_site.views:create_blueprint
invenio_assets.webpack =
    my_site_theme = my_site.webpack:theme
# ...other entry points for Celery tasks, models, CLI commands, etc.
```

#### After: `site/pyproject.toml`

```toml title="site/pyproject.toml"
[project]
name = "my-site" # (1)!
version = "1.0.0" # (2)!
description = "My Site customizations for Invenio RDM."
# (3)!

[project.entry-points."invenio_base.blueprints"] # (4)!
my_site_views = "my_site.views:create_blueprint"
[project.entry-points."invenio_assets.webpack"]
my_site_theme = "my_site.webpack:theme"
# ...other entry points for Celery tasks, models, CLI commands, etc.

[build-system] # (5)!
requires = ["hatchling"]
build-backend = "hatchling.build"
```

1. Package name should match what's referenced in the root `pyproject.toml`
2. Version is a required field in `pyproject.toml`
3. We don't need to define any dependencies here, since they are managed at the root `pyproject.toml`
4. Entry points for blueprints, assets, Celery tasks, etc. remain similar
5. Modern build system - `hatchling` is recommended for pure Python packages

### Update Invenio configuration 📜

Update the `.invenio` configuration file so that `invenio-cli` uses `uv` commands instead of `pipenv` for dependency management:

```ini title=".invenio" hl_lines="4"
[cli]
flavour = RDM
logfile = /logs/invenio-cli.log
python_package_manager = uv

[cookiecutter]
project_name = My Site
...
```

### Clean up old files 📜

Remove any old files:

```bash
rm Pipfile Pipfile.lock site/setup.cfg site/setup.py site/MANIFEST.in
```

### Generate new Python dependencies lockfile

Generate the `uv.lock` file:

```bash
invenio-cli packages lock
```

### Update Dockerfile

#### Before: Docker with Pipenv

```dockerfile title="Dockerfile"
...
COPY site ./site
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system
...
```

#### After: Docker with uv

```dockerfile title="Dockerfile"
...
# Python and uv configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Cache directory for uv's package downloads - persisted across builds with Docker BuildKit
    UV_CACHE_DIR=/opt/.cache/uv \
    # Pre-compile Python bytecode for faster startup times in production
    UV_COMPILE_BYTECODE=1 \
    # Strictly use versions from uv.lock file, failing if lock file is outdated
    UV_FROZEN=1 \
    # Copy packages instead of symlinking - required for Docker's layered filesystem
    UV_LINK_MODE=copy \
    # Use the system's Python installation instead of uv managing Python versions
    UV_NO_MANAGED_PYTHON=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_PROJECT_ENVIRONMENT=/usr/ \
    UV_PYTHON_DOWNLOADS=never \
    # Require and verify package hashes match those in the lock file
    UV_REQUIRE_HASHES=1 \
    UV_VERIFY_HASHES=1

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# First sync: install only external dependencies without workspace packages
RUN --mount=type=cache,target=/opt/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --no-install-workspace --no-editable

# Copy static code, assets, and configuration files
COPY site ./site
COPY legacy ./legacy

COPY ./docker/uwsgi/ ${INVENIO_INSTANCE_PATH}
COPY ./invenio.cfg ${INVENIO_INSTANCE_PATH}
COPY ./templates/ ${INVENIO_INSTANCE_PATH}/templates/
COPY ./app_data/ ${INVENIO_INSTANCE_PATH}/app_data/
COPY ./translations ${INVENIO_INSTANCE_PATH}/translations
COPY ./ .

# Second sync: install workspace packages
RUN --mount=type=cache,target=/opt/.cache/uv \
    uv sync --frozen --no-dev
...
```

### Update CI/CD Configuration

#### Before: GitHub Actions with Pipenv

```yaml
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
    cache: pip
    cache-dependency-path: Pipfile.lock

- name: Install dependencies
  run: |
    pip install "pipenv==2023.12.1"
    pipenv install --deploy --system
    pip install -e ./site
    pip freeze
```

#### After: GitHub Actions with uv
```yaml
- name: Install uv # (1)!
  uses: astral-sh/setup-uv@v5
  with:
    python-version: ${{ matrix.python-version }}
    enable-cache: true # (2)!

- name: Install dependencies
  run: | # (3)!
    uv sync --locked
    uv pip list
```

1. Use the official uv GitHub Action instead of installing via pip
2. uv has built-in caching that's faster than pip's cache
3. `--locked` ensures exact versions from `uv.lock` are installed (like `pipenv install --deploy`).

## Next steps

After completing the migration:

1. Test your application to ensure all dependencies are correctly installed
2. Update your development team's documentation with the new uv commands
3. Verify that your CI/CD pipelines work with the new configuration
4. Consider removing any old Pipenv-specific scripts or documentation
