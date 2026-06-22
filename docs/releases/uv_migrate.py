#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "tomlkit",
#     "click",
# ]
# ///
"""
Migration script to convert from Pipenv to uv.

This script:
- Converts root Pipfile to pyproject.toml
- Converts site/setup.cfg to site/pyproject.toml
- Updates .invenio configuration
- Removes old unnecessary files (Pipfile, Pipfile.lock, setup.cfg, setup.py, MANIFEST.in)
"""

import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import click
import tomlkit
import tomllib


@dataclass
class ProjectConfig:
    """Configuration for project conversion."""

    # Package names
    app_package_name: str
    site_package_name: str
    # Author info
    author_name: str
    author_email: str
    python_version: str
    # File paths
    pipfile_path: Path
    setup_cfg_path: Path
    root_pyproject_path: Path
    site_pyproject_path: Path
    invenio_path: Path
    # Dependencies
    site_dependencies: Optional[List[str]] = None
    site_dev_dependencies: Optional[List[str]] = None


def parse_dependencies(deps_string: str) -> List[str]:
    """Parse dependencies from a multiline string, filtering comments and empty lines."""
    return [
        dep.strip()
        for dep in deps_string.split("\n")
        if dep.strip() and not dep.strip().startswith("#")
    ]


def create_dependency_sort_key(site_package_name: str):
    """Create a sort key function for dependency ordering."""

    def dependency_sort_key(dep: str) -> tuple:
        pkg_name = (
            dep.split("[")[0]
            .split("=")[0]
            .split("<")[0]
            .split(">")[0]
            .split("!")[0]
            .split("~")[0]
            .strip()
        )

        if pkg_name == "invenio-app-rdm":
            return (0, pkg_name)
        elif pkg_name == site_package_name:
            return (1, pkg_name)
        elif pkg_name.startswith("invenio-"):
            return (2, pkg_name)
        else:
            return (3, pkg_name)

    return dependency_sort_key


def convert_toml_value(value, key_path=""):
    """Convert Python values to tomlkit values with appropriate formatting."""
    if isinstance(value, dict):
        is_uv_source = key_path.startswith("tool.uv.sources.")
        is_entry_point = key_path.startswith("project.entry-points")
        is_tool_section = key_path.startswith("tool.")
        has_simple_values = all(
            isinstance(v, (str, int, float, bool)) for v in value.values()
        )
        is_small_dict = len(value) <= 3

        use_inline_table = is_uv_source or (
            not is_entry_point
            and not is_tool_section
            and has_simple_values
            and is_small_dict
        )

        if use_inline_table:
            inline_table = tomlkit.inline_table()
            for k, v in value.items():
                inline_table[k] = v
            return inline_table
        else:
            table = tomlkit.table()
            for k, v in value.items():
                nested_key = f"{key_path}.{k}" if key_path else k
                table[k] = convert_toml_value(v, nested_key)
            return table
    elif isinstance(value, list):
        if len(value) > 0 and isinstance(value[0], dict) and "name" in value[0]:
            # Authors need inline table format per TOML spec
            array = tomlkit.array()
            for item in value:
                inline_table = tomlkit.inline_table()
                for k, v in item.items():
                    inline_table[k] = v
                array.append(inline_table)
            return array
        elif len(value) > 1:
            # Multi-line format improves readability for dependency lists
            array = tomlkit.array()
            for item in value:
                array.append(item)
            array.multiline(True)
            return array
        else:
            return value
    else:
        return value


def add_toml_section(doc, key, value):
    """Add a section to the TOML document with proper nesting."""
    if "." in key:
        if key.startswith("project.entry-points."):
            # Entry points need manual handling to avoid tomlkit quote escaping bugs
            entry_point_name = key[len("project.entry-points.") :]
            if "project" not in doc:
                doc["project"] = tomlkit.table()
            if "entry-points" not in doc["project"]:
                doc["project"]["entry-points"] = tomlkit.table()

            doc["project"]["entry-points"][entry_point_name] = convert_toml_value(
                value, key
            )
        else:
            parts = key.split(".")
            current = doc
            for part in parts[:-1]:
                if part not in current:
                    current[part] = tomlkit.table()
                current = current[part]

            current[parts[-1]] = convert_toml_value(value, key)
    else:
        doc[key] = convert_toml_value(value, key)


def write_toml(data: Dict[str, Any], file_path: Path) -> None:
    """Write data to a TOML file using tomlkit for proper formatting."""
    doc = tomlkit.document()

    for key, value in data.items():
        add_toml_section(doc, key, value)

    with open(file_path, "w") as f:
        f.write(tomlkit.dumps(doc))


def parse_pipfile_dependency(dep_spec: Union[str, dict]) -> Optional[str]:
    """Parse a Pipfile dependency specification and convert to PEP 508 format."""
    if isinstance(dep_spec, str):
        return dep_spec

    if isinstance(dep_spec, dict):
        if "git" in dep_spec:
            git_url = dep_spec["git"]
            if "ref" in dep_spec:
                return f"@ git+{git_url}@{dep_spec['ref']}"
            else:
                return f"@ git+{git_url}"

        if "path" in dep_spec:
            path = dep_spec["path"]
            if path == "./site":
                return None  # Site dependency handled as workspace member
            else:
                return f"@ file://{path}"

        parts = []
        if "version" in dep_spec:
            parts.append(dep_spec["version"])

        if "extras" in dep_spec:
            extras = dep_spec["extras"]
            if isinstance(extras, list):
                extras_str = ",".join(extras)
            else:
                extras_str = extras
            return f"[{extras_str}]" + ("".join(parts) if parts else "")

        return "".join(parts) if parts else ""

    return str(dep_spec)


def extract_site_dependencies(setup_cfg_path: Path) -> tuple:
    """Extract dependencies and dev dependencies from site/setup.cfg."""
    config = configparser.ConfigParser()
    config.read(setup_cfg_path)

    dependencies = []
    dev_dependencies = []

    if config.has_section("options") and config.has_option(
        "options", "install_requires"
    ):
        install_requires = config.get("options", "install_requires").strip()
        if install_requires:
            dependencies.extend(parse_dependencies(install_requires))

    if config.has_section("options.extras_require"):
        for key, value in config.items("options.extras_require"):
            if key == "tests":
                deps = [dep.strip() for dep in value.split("\n") if dep.strip()]
                dev_dependencies.extend(deps)

    return dependencies, dev_dependencies


def extract_entry_points_from_setup_cfg(
    setup_cfg_path: Path,
) -> Dict[str, Dict[str, str]]:
    """Extract entry points from setup.cfg file using manual parsing."""
    entry_points = {}

    with open(setup_cfg_path, "r") as f:
        content = f.read()

    lines = content.split("\n")
    in_entry_points = False
    current_group = None

    for line in lines:
        stripped = line.strip()
        if stripped == "[options.entry_points]":
            in_entry_points = True
            continue
        elif stripped.startswith("[") and in_entry_points:
            break
        elif in_entry_points and stripped:
            if "=" in stripped and not stripped.endswith("="):
                if current_group:
                    key, value = stripped.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if current_group not in entry_points:
                        entry_points[current_group] = {}
                    entry_points[current_group][key] = value
            elif stripped.endswith("="):
                current_group = stripped[:-1].strip()
                if current_group not in entry_points:
                    entry_points[current_group] = {}

    return entry_points


def convert_pipfile_to_pyproject(config: ProjectConfig) -> None:
    """Convert Pipfile to pyproject.toml."""
    click.echo(f"Converting {config.pipfile_path} to {config.root_pyproject_path}")

    with open(config.pipfile_path, "rb") as f:
        pipfile_data = tomllib.load(f)

    # Extract basic info
    packages = pipfile_data.get("packages", {})
    dev_packages = pipfile_data.get("dev-packages", {})
    requires = pipfile_data.get("requires", {})

    # Build dependencies list
    dependencies = []
    uv_sources = {}
    workspace_members = []

    for name, spec in packages.items():
        # Replace uwsgi with pyuwsgi for better wheel support
        if name == "uwsgi":
            name = "pyuwsgi"
            click.secho(
                "  ℹ️ Replaced uwsgi with pyuwsgi in Pipfile dependencies (for better wheel support)",
                fg="blue",
            )

        if isinstance(spec, dict) and "path" in spec:
            path = spec["path"]
            if path == "./site":
                dependencies.append(config.site_package_name)
                uv_sources[config.site_package_name] = {"workspace": True}
                workspace_members.append("site")
        elif isinstance(spec, dict) and "git" in spec:
            git_url = spec["git"]
            ref = spec.get("ref", "main")
            dependencies.append(name)
            uv_sources[name] = {"git": git_url, "rev": ref}
        else:
            dep_str = parse_pipfile_dependency(spec)
            if dep_str is None:
                continue  # Skip ignored dependencies
            if isinstance(spec, dict) and "extras" in spec:
                extras = spec["extras"]
                if isinstance(extras, list):
                    extras_str = ",".join(extras)
                else:
                    extras_str = extras
                version = spec.get("version", "")
                dependencies.append(f"{name}[{extras_str}]{version}")
            else:
                dependencies.append(f"{name}{dep_str}")

    if config.site_dependencies:
        dependencies.extend(config.site_dependencies)

    dependencies = list(set(dependencies))
    dependencies = sorted(
        dependencies, key=create_dependency_sort_key(config.site_package_name)
    )

    # Build dev dependencies
    dev_dependencies = []
    for name, spec in dev_packages.items():
        dep_str = parse_pipfile_dependency(spec)
        dev_dependencies.append(f"{name}{dep_str}")

    if config.site_dev_dependencies:
        dev_dependencies.extend(config.site_dev_dependencies)

    if dev_dependencies:
        dev_dependencies = sorted(list(set(dev_dependencies)))
        # Remove check-manifest as it's no longer needed with uv
        dev_dependencies = [
            dep for dep in dev_dependencies if not dep.startswith("check-manifest")
        ]

    python_version = requires.get("python_version", config.python_version)

    pyproject_data = {
        "project": {
            "name": config.app_package_name,
            "version": "1.0.0",
            "authors": [{"name": config.author_name, "email": config.author_email}],
            "license": "MIT",
            "requires-python": f">={python_version}",
            "dependencies": dependencies,
        }
    }

    if dev_dependencies:
        pyproject_data["dependency-groups"] = {"dev": dev_dependencies}

    if uv_sources or workspace_members:
        pyproject_data["tool"] = {"uv": {}}
        if uv_sources:
            pyproject_data["tool"]["uv"]["sources"] = uv_sources
        if workspace_members:
            pyproject_data["tool"]["uv"]["workspace"] = {"members": workspace_members}

    write_toml(pyproject_data, config.root_pyproject_path)
    click.secho(f"✓ Created {config.root_pyproject_path}", fg="green")


def parse_attr_version(attr_spec: str) -> str:
    """Parse attr: version specification and return the __version__ module_path."""
    attr_path = attr_spec.replace("attr:", "").strip()
    *module_parts, _ = attr_path.split(".")

    # Convert module path to file path
    # e.g. "my_site" -> "my_site/__init__.py"
    module_path = "/".join(module_parts)
    return f"{module_path}/__init__.py"


def convert_setup_cfg_to_pyproject(config: ProjectConfig) -> None:
    """Convert setup.cfg to pyproject.toml, preserving all entry points."""
    click.echo(f"Converting {config.setup_cfg_path} to {config.site_pyproject_path}")

    parser = configparser.ConfigParser()
    parser.read(config.setup_cfg_path)

    metadata = {}
    if parser.has_section("metadata"):
        for key, value in parser.items("metadata"):
            metadata[key] = value

    options = {}
    if parser.has_section("options"):
        for key, value in parser.items("options"):
            options[key] = value

    # Handle version - check if it's dynamic (attr:) or static
    version_config = {}
    version_file_path = None
    version_value = metadata.get("version", "1.0.0")

    if version_value.startswith("attr:"):
        # Dynamic version using attr: specification
        try:
            version_file_path = parse_attr_version(version_value)
            version_config = {"dynamic": ["version"]}
            click.secho(
                f"  Found dynamic version: {version_value} -> {version_file_path}",
                fg="blue",
            )
        except ValueError as e:
            click.secho(f"  Warning: {e}, using static version instead")
            version_config = {"version": "1.0.0"}
    else:
        # Static version
        version_config = {"version": version_value}

    project_data = {
        "name": config.site_package_name,
        "description": metadata.get(
            "description", f"{config.site_package_name} customizations for Invenio RDM."
        ),
        "license": metadata.get("license", "MIT"),
        **version_config,
    }

    if "author" in metadata:
        authors = [{"name": metadata["author"]}]
        if "author_email" in metadata:
            authors[0]["email"] = metadata["author_email"]
        project_data["authors"] = authors

    # Dependencies are not included for site package (handled at root level)
    entry_points = {}
    if parser.has_section("options.entry_points"):
        entry_points = extract_entry_points_from_setup_cfg(config.setup_cfg_path)

    pyproject_data = {"project": project_data}

    if entry_points:
        for group_name, group_entries in entry_points.items():
            if group_entries:
                section_key = f"project.entry-points.{group_name}"
                pyproject_data[section_key] = group_entries

    pyproject_data["build-system"] = {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }

    tool_configs = {}

    # Add hatchling version configuration if dynamic version is used
    if "dynamic" in project_data and "version" in project_data["dynamic"]:
        tool_configs["hatch"] = {"version": {"path": version_file_path}}
        click.secho(
            f"  Added hatchling version config: path = {version_file_path}",
            fg="blue",
        )

    if parser.has_section("tool:pytest"):
        tool_configs["pytest"] = {"ini_options": {}}
        for key, value in parser.items("tool:pytest"):
            tool_configs["pytest"]["ini_options"][key] = value

    if parser.has_section("isort"):
        tool_configs["isort"] = {}
        for key, value in parser.items("isort"):
            tool_configs["isort"][key] = value

    if parser.has_section("pydocstyle"):
        tool_configs["pydocstyle"] = {}
        for key, value in parser.items("pydocstyle"):
            tool_configs["pydocstyle"][key] = value

    if tool_configs:
        for tool_name, tool_config in tool_configs.items():
            pyproject_data[f"tool.{tool_name}"] = tool_config

    write_toml(pyproject_data, config.site_pyproject_path)
    click.secho(f"✓ Created {config.site_pyproject_path}", fg="green")


def update_invenio_config(config: ProjectConfig) -> None:
    """Update .invenio configuration to use uv."""
    if not config.invenio_path.exists():
        click.secho(f"⚠ {config.invenio_path} not found, skipping", fg="yellow")
        return

    parser = configparser.ConfigParser()
    parser.read(config.invenio_path)

    # Update python_package_manager
    if not parser.has_section("cli"):
        parser.add_section("cli")

    parser.set("cli", "python_package_manager", "uv")

    with open(config.invenio_path, "w") as f:
        parser.write(f)

    click.secho(f"✓ Updated {config.invenio_path} to use uv", fg="green")


def cleanup_old_files(root_dir: Path) -> None:
    """Remove old files that are no longer needed after migration."""
    site_dir = root_dir / "site"

    # Files to remove
    files_to_remove = [
        root_dir / "Pipfile",
        root_dir / "Pipfile.lock",
        site_dir / "setup.cfg",
        site_dir / "setup.py",
        site_dir / "MANIFEST.in",
    ]

    removed_files = []

    for file_path in files_to_remove:
        if file_path.exists():
            file_path.unlink()
            removed_files.append(file_path)
            click.secho(f"🗑️ Removed {file_path}", fg="yellow")

    if removed_files:
        click.secho(f"✓ Cleaned up {len(removed_files)} old files", fg="green")
    else:
        click.secho("ℹ️ No old files to clean up", fg="blue")


@click.command()
@click.option(
    "--root-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd(),
    help="Root directory of the project (default: current directory)",
)
@click.option(
    "--project-name",
    help="Name for the project (auto-detected from '.invenio' project_shortname if not provided)",
)
@click.option(
    "--cleanup",
    is_flag=True,
    help="Remove old files (Pipfile, setup.cfg, etc.) after migration",
)
def main(root_dir: Path, project_name: Optional[str], cleanup: bool):
    """Migrate from Pipenv to uv."""
    site_dir = root_dir / "site"

    if project_name is None:
        invenio_path = root_dir / ".invenio"
        if not invenio_path.exists():
            raise click.UsageError(
                "No .invenio file found and no --project-name provided. "
                "Either provide --project-name or ensure .invenio file exists."
            )

        try:
            config = configparser.ConfigParser()
            config.read(invenio_path)
            if "cookiecutter" not in config:
                raise click.UsageError(
                    "No [cookiecutter] section found in .invenio file. "
                    "Please provide --project-name manually."
                )

            cookiecutter_cfg = config["cookiecutter"]
            project_shortname = cookiecutter_cfg.get("project_shortname")
            if not project_shortname:
                raise click.UsageError(
                    "No project_shortname found in .invenio file. "
                    "Please provide --project-name manually."
                )

            # Extract author and Python version from .invenio
            author_name = cookiecutter_cfg.get("author_name")
            author_email = cookiecutter_cfg.get("author_email")
            python_version = cookiecutter_cfg.get("python_version")

            # Use defaults and warn if values not found
            if not author_name:
                author_name = "CHANGE_ME"
                click.secho(
                    "⚠️  No author_name found in .invenio file, using 'CHANGE_ME'",
                    fg="yellow",
                )
            if not author_email:
                author_email = "change@me.org"
                click.secho(
                    "⚠️  No author_email found in .invenio file, using 'change@me.org'",
                    fg="yellow",
                )
            if not python_version:
                python_version = "3.12"
                click.secho(
                    "⚠️  No python_version found in .invenio file, using '3.12'",
                    fg="yellow",
                )

            # Root app needs different name to avoid package conflicts
            site_project_name = project_shortname
            app_project_name = f"{project_shortname}-app"
            click.secho(
                f"📦 Auto-detected project names from .invenio - app: '{app_project_name}', site: '{site_project_name}'",
                fg="blue",
            )
        except configparser.Error as e:
            raise click.UsageError(f"Could not parse .invenio file: {e}")
        except Exception as e:
            raise click.UsageError(f"Could not read .invenio file: {e}")
    else:
        # Root app needs different name to avoid package conflicts
        site_project_name = project_name
        app_project_name = f"{project_name}-app"
        # Use defaults when project name is provided manually
        author_name = "CHANGE_ME"
        author_email = "change@me.org"
        python_version = "3.12"
        click.secho(
            "⚠️  Using default values for author and Python version", fg="yellow"
        )
        click.secho(
            f"📦 Using provided project names - app: '{app_project_name}', site: '{site_project_name}'",
            fg="blue",
        )

    click.secho(
        f"🚀 Starting migration from Pipenv to uv in {root_dir}", fg="cyan", bold=True
    )

    pipfile_path = root_dir / "Pipfile"
    if not pipfile_path.exists():
        raise click.UsageError(f"No Pipfile found in {root_dir}")

    setup_cfg_path = site_dir / "setup.cfg"
    if not setup_cfg_path.exists():
        raise click.UsageError(f"No setup.cfg found in {site_dir}")

    try:
        site_dependencies, site_dev_dependencies = extract_site_dependencies(
            setup_cfg_path
        )

        project_config = ProjectConfig(
            app_package_name=app_project_name,
            site_package_name=site_project_name,
            author_name=author_name,
            author_email=author_email,
            python_version=python_version,
            pipfile_path=pipfile_path,
            setup_cfg_path=setup_cfg_path,
            root_pyproject_path=root_dir / "pyproject.toml",
            site_pyproject_path=site_dir / "pyproject.toml",
            invenio_path=root_dir / ".invenio",
            site_dependencies=site_dependencies,
            site_dev_dependencies=site_dev_dependencies,
        )

        convert_pipfile_to_pyproject(project_config)
        convert_setup_cfg_to_pyproject(project_config)
        update_invenio_config(project_config)

        if cleanup:
            cleanup_old_files(root_dir)
        else:
            click.secho(
                "ℹ️ Old files (Pipfile, setup.cfg, etc.) were not removed", fg="yellow"
            )
            click.secho(
                "   Run again with --cleanup to remove them after testing", fg="yellow"
            )

        click.secho("\n✅ Migration completed successfully!", fg="green", bold=True)
        click.secho("\nNext steps:", fg="cyan", bold=True)
        click.secho("1. Review the generated pyproject.toml files")
        click.secho("2. Run 'invenio-cli packages lock' to generate the 'uv.lock' file")
        click.secho("3. Test your application")
        click.secho("4. Update CI/CD configurations")
        click.secho("5. Update your Dockerfile")

    except Exception as e:
        click.secho(f"❌ Migration failed: {e}", fg="red", err=True)
        raise


if __name__ == "__main__":
    main()
