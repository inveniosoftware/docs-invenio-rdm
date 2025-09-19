# Invenio commands reference

The `invenio` tool provides application management and administration commands. These commands are executed within the application context and are used for managing users, roles, access permissions, and other application-level operations.

Following is an overview of all command groups in `invenio`:

| Command Group    | Description                                              |
| :--------------- | :------------------------------------------------------- |
| `access`         | Account commands - manage access permissions and actions |
| `alembic`        | Perform database migrations                              |
| `collect`        | Collect static files                                     |
| `communities`    | Invenio communities commands                             |
| `db`             | Database commands                                        |
| `domains`        | Domain commands                                          |
| `files`          | File management commands                                 |
| `i18n`           | Internationalization commands                            |
| `identity-cache` | Invenio identity cache commands                          |
| `index`          | Manage search indices                                    |
| `instance`       | Instance commands                                        |
| `limiter`        | Flask-Limiter maintenance & utility commands             |
| `pid`            | PID-Store management commands                            |
| `queues`         | Manage events queue                                      |
| `rdm`            | Invenio app RDM commands                                 |
| `rdm-records`    | InvenioRDM records commands                              |
| `roles`          | Role commands - manage user roles                        |
| `routes`         | Show the routes for the app                              |
| `run`            | Run a development server                                 |
| `shell`          | Runs a shell in the app context                          |
| `stats`          | Statistics commands                                      |
| `tokens`         | OAuth2 server token commands                             |
| `users`          | User commands - manage user accounts                     |
| `vocabularies`   | Vocabularies command                                     |
| `webpack`        | Webpack commands                                         |

## `invenio access` commands

Account commands - manage access permissions and actions.

| Command | Description                           |
| :------ | :------------------------------------ |
| allow   | Allow action.                         |
| deny    | Deny actions.                         |
| list    | List all registered actions.          |
| remove  | Remove existing action authorization. |
| show    | Show all assigned actions.            |

## `invenio alembic` commands

Perform database migrations.

| Command   | Description                                                       |
| :-------- | :---------------------------------------------------------------- |
| branches  | Show the list of revisions that have more than one next revision. |
| current   | Show the list of current revisions.                               |
| downgrade | Run migration to downgrade the database.                          |
| heads     | Show the list of revisions that have no child revisions.          |
| log       | Show the list of revisions in the order they will run.            |
| merge     | Generate a merge revision.                                        |
| mkdir     | Create the migration directory if it does not exist.              |
| revision  | Generate a new revision.                                          |
| show      | Show the given revisions.                                         |
| stamp     | Set the current revision without running migrations.              |
| upgrade   | Run migrations to upgrade the database.                           |

## `invenio collect` commands

Collect static files.

| Command | Description           |
| :------ | :-------------------- |
| collect | Collect static files. |

### **`collect`**

Collect static files.

**Usage**

```bash
invenio collect [OPTIONS]
```

**Options**

| Option          | Description           |
| :-------------- | :-------------------- |
| `-v, --verbose` | Enable verbose output |

## `invenio communities` commands

| Command       | Description                                    |
| :------------ | :--------------------------------------------- |
| custom-fields | Communities custom fields commands.            |
| demo          | Create 100 fake communities for demo purposes. |
| rebuild-index | Rebuild index.                                 |

## `invenio db` commands

Database commands.

| Command | Description      |
| :------ | :--------------- |
| create  | Create tables.   |
| destroy | Drop database.   |
| drop    | Drop tables.     |
| init    | Create database. |

## `invenio domains` commands

| Command | Description    |
| :------ | :------------- |
| create  | Create domain. |

## `invenio files` commands

File management commands.

| Command  | Description       |
| :------- | :---------------- |
| bucket   | Manage buckets.   |
| location | Manage locations. |

## `invenio i18n` commands

Internationalization commands.

| Command                    | Description                                          |
| :------------------------- | :--------------------------------------------------- |
| distribute-js-translations | Distribute package‑specific JavaScript translations. |
| fetch-from-transifex       | Retrieve package translations from Transifex.        |

## `invenio identity-cache` commands

Invenio identity cache commands.

| Command | Description            |
| :------ | :--------------------- |
| clear   | Clears identity cache. |

## `invenio index` commands

Manage search indices.

| Command | Description                                 |
| :------ | :------------------------------------------ |
| check   | Check search engine version.                |
| create  | Create a new index.                         |
| delete  | Delete index by its name.                   |
| destroy | Destroy all indexes.                        |
| init    | Initialize registered aliases and mappings. |
| list    | List indices.                               |
| put     | Index input data.                           |
| queue   | Manage indexing queue.                      |
| reindex | Reindex all records.                        |
| run     | Run bulk record indexing.                   |
| update  | Update mappings of existing index.          |

## `invenio instance` commands

Instance commands.

| Command            | Description                                          |
| :----------------- | :--------------------------------------------------- |
| entrypoints        | List defined entry points.                           |
| migrate-secret-key | Call entry points exposed for the SECRET_KEY change. |

## `invenio limiter` commands

Flask-Limiter maintenance & utility commands.

| Command | Description                                          |
| :------ | :--------------------------------------------------- |
| clear   | Clear limits for a specific key.                     |
| config  | View the extension configuration.                    |
| limits  | Enumerate details about all routes with rate limits. |

## `invenio pid` commands

PID-Store management commands.

| Command     | Description                                 |
| :---------- | :------------------------------------------ |
| assign      | Assign persistent identifier.               |
| create      | Create new persistent identifier.           |
| dereference | Show linked persistent identifier(s).       |
| get         | Get an object behind persistent identifier. |
| unassign    | Unassign persistent identifier.             |

## `invenio queues` commands

Manage events queue.

| Command | Description                  |
| :------ | :--------------------------- |
| declare | Initialize the given queues. |
| delete  | Delete the given queues.     |
| list    | List configured queues.      |
| purge   | Purge the given queues.      |

## `invenio rdm` commands

Invenio app RDM commands.

| Command             | Description                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| fixtures            | Create the fixtures.                                                                |
| pages               | Static pages.                                                                       |
| rebuild-all-indices | Schedule reindexing of (all) items for search with optional selection and ordering. |

### **`rdm fixtures`**

Create the fixtures.

### **`rdm pages`**

see [Static pages](../operate/customize/static_pages.md).

### **`rdm pages create`**

**Options**

- `-f`, `--force` Creates static pages.

### **`rdm rebuild-all-indices`**

Reindex all services with optional selecting and ordering.

**Options**

- `-o`, `--order` Comma-separated list of services to reindex in the specified order. If not provided, all services will be reindexed.
  e.g.:

```bash
invenio rdm rebuild-all-indices -o users,communities,records,requests,request_events
```

if you don't specify services, The following services will be reindexed:

`users, groups, domains, communities, members, records, record-media-files, affiliations, awards, funders, names, subjects, vocabularies, requests, request_events, oaipmh-server`

Note that the users, groups, and members use bulk indexing and rely on celery running. They will not be reindexed if celery is not running.

This command does not impact usage statistics indexes. You need to manually restore statistics indexes [from a backup](../operate/ops/backup_search_indices.md).

## `invenio rdm-records` commands

InvenioRDM records commands.

| Command        | Description                                       |
| :------------- | :------------------------------------------------ |
| add-to-fixture | Add or update new entries to existing fixture.    |
| custom-fields  | InvenioRDM custom fields commands.                |
| demo           | Create fake demo data.                            |
| fixtures       | Create the fixtures required for record creation. |
| rebuild-index  | Reindex all drafts, records and vocabularies.     |

## `invenio roles` commands

Role commands - manage user roles.

| Command | Description            |
| :------ | :--------------------- |
| add     | Add user to role.      |
| create  | Create a role.         |
| remove  | Remove user from role. |

### **`roles create`**

Create a new role.

**Usage**

```bash
invenio roles create ROLE [OPTIONS]
```

**Options**

- `-d`, `--description`: Description for the role

**Example**

```bash
invenio roles create admin -d "Administrator role"
```

### **`roles add`**

Add a user to a role.

**Usage**

```bash
invenio roles add USER ROLE
```

**Example**

```bash
invenio roles add user@example.com admin
```

### **`roles remove`**

Remove a user from a role.

**Usage**

```bash
invenio roles remove USER ROLE
```

**Example**

```bash
invenio roles remove user@example.com admin
```

## `invenio routes` commands

Show all registered routes with endpoints and methods.

| Command | Description                                            |
| :------ | :----------------------------------------------------- |
| routes  | Show all registered routes with endpoints and methods. |

### **`routes`**

Show all registered routes with endpoints and methods.

**Usage**

```bash
invenio routes [OPTIONS]
```

**Options**

| Option                                                | Description                                                                                            |
| :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `-s, --sort [endpoint\|methods\|domain\|rule\|match]` | Method to sort routes by. 'match' is the order that Flask will match routes when dispatching a request |
| `--all-methods`                                       | Show HEAD and OPTIONS methods                                                                          |

## `invenio run` commands

Run a development server.

| Command | Description                     |
| :------ | :------------------------------ |
| run     | Run a local development server. |

### **`run`**

Run a local development server.

This server is for development purposes only. It does not provide the stability, security, or performance of production WSGI servers.

**Usage**

```bash
invenio run [OPTIONS]
```

**Options**

| Option                               | Description                                                                                                       |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `--debug / --no-debug`               | Set debug mode                                                                                                    |
| `-h, --host TEXT`                    | The interface to bind to                                                                                          |
| `-p, --port INTEGER`                 | The port to bind to                                                                                               |
| `--cert PATH`                        | Specify a certificate file to use HTTPS                                                                           |
| `--key FILE`                         | The key file to use when specifying a certificate                                                                 |
| `--reload / --no-reload`             | Enable or disable the reloader. By default the reloader is active if debug is enabled                             |
| `--debugger / --no-debugger`         | Enable or disable the debugger. By default the debugger is active if debug is enabled                             |
| `--with-threads / --without-threads` | Enable or disable multithreading                                                                                  |
| `--extra-files PATH`                 | Extra files that trigger a reload on change. Multiple paths are separated by ':'                                  |
| `--exclude-patterns PATH`            | Files matching these fnmatch patterns will not trigger a reload on change. Multiple patterns are separated by ':' |

## `invenio stats` commands

Statistics commands.

| Command      | Description                      |
| :----------- | :------------------------------- |
| aggregations | Aggregation management commands. |
| events       | Event management commands.       |

**Usage**

```bash
invenio stats <command> [OPTIONS]
```

## `invenio tokens` commands

OAuth2 server token commands.

| Command | Description                    |
| :------ | :----------------------------- |
| create  | Create a personal OAuth token. |
| delete  | Delete a personal OAuth token. |

**Usage**

```bash
invenio tokens <command> [OPTIONS]
```

## `invenio vocabularies` commands

Vocabularies command.

| Command | Description                                           |
| :------ | :---------------------------------------------------- |
| convert | Convert a vocabulary to a new format.                 |
| delete  | Delete all items or a specific one of the vocabulary. |
| import  | Import a vocabulary.                                  |
| update  | Import a vocabulary.                                  |

See [ROR dataset import](../operate/customize/vocabularies/funding.md#funders-ror).

**Usage**

```bash
invenio vocabularies <command> [OPTIONS]
```

## `invenio webpack` commands

Webpack commands.

| Command  | Description                                |
| :------- | :----------------------------------------- |
| build    | Run NPM build-script.                      |
| buildall | Create, install and build webpack project. |
| clean    | Remove created webpack project.            |
| create   | Create webpack project.                    |
| install  | Run NPM install.                           |
| run      | Run an NPM script.                         |

**Usage**

```bash
invenio webpack <command> [OPTIONS]
```

## `invenio users` commands

User account management commands.

| Command    | Description        |
| :--------- | :----------------- |
| create     | Create a user.     |
| activate   | Activate a user.   |
| deactivate | Deactivate a user. |

### **`users create`**

Create a new user account.

**Usage**

```bash
invenio users create EMAIL [OPTIONS]
```

**Arguments**

- `EMAIL`: User's email address (required)

**Options**

- `--password <password>`: Set user password (if not provided, random password is generated)
- `--active`: Activate the user account immediately
- `--confirm`: Confirm the user account immediately (skip email verification)

**Examples**

```bash
# Create a basic user (inactive, unconfirmed)
invenio users create user@example.org

# Create an active and confirmed user
invenio users create admin@example.org --active --confirm

# Create user with specific password
invenio users create user@example.org --password mypassword123 --active --confirm
```

### **`users activate`**

Activate a user account.

**Usage**

```bash
invenio users activate EMAIL
```

### **`users deactivate`**

Deactivate a user account.

**Usage**

```bash
invenio users deactivate EMAIL
```

## `invenio shell` commands

Runs a shell in the app context.

| Command | Description                      |
| :------ | :------------------------------- |
| shell   | Runs a shell in the app context. |

### **`shell`**

Open an interactive Python shell in the application context with access to all application components.

Runs an interactive Python shell in the context of a given Flask application. The application will populate the default namespace of this shell according to its configuration.

**Usage**

```bash
invenio shell [OPTIONS] [IPYTHON_ARGS]...
```

This command is useful for:

- Debugging and testing
- Running one-off data manipulation scripts
- Accessing application components directly
