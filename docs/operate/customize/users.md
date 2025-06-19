# Manage users and roles

## Add users via fixtures

You can load a default set of users into your InvenioRDM system using fixtures, similar to how you manage vocabularies. This method relies on a `users.yaml` file located within your application's data folder.

The file `users.yaml` contains a list of users to create, and is stored in the
root of the `app_data` folder.

```
app_data/
└── users.yaml
```

The content of the file is as follows:

```yaml
#list of users:
- email: <string>
  username: <string>
  full_name: <string>
  affiliations: <string>
  active: <bool>
  confirmed: <bool>
  password: <string>
  roles: <array of strings>
  allow: <array of strings>
```

- `email` : Email of the user.
- `username` : Username of the user (optional).
- `full_name`: Name of the user (optional).
- `affiliations` : Affiliations of the user (optional).
- `active` : Is the user active or not.
- `confirmed` : Is the user confirmed or not (optional).
- `password` : Their password. If empty, a random one is generated.
- `roles` : Array of roles the user has. The roles must already be present in the DB.
- `allow` : Array of action needs the user has.

If the file is not provided, InvenioRDM creates an `admin` user with the email
`admin@inveniosoftware.org` (and a random password). If the file is provided
but is empty, no default user is created.

!!! tip "About random passwords"

    A random password is automatically generated when the field `password` is empty (or for the `admin` user).
    You can define users' passwords also by setting the variable `RDM_RECORDS_USER_FIXTURE_PASSWORDS`
    in your `invenio.cfg`:

    ```python
    RDM_RECORDS_USER_FIXTURE_PASSWORDS = {
       'admin@inveniosoftware.org': 'supersecret123',
       'test@inveniosoftware.org': 'mypsw987',
    }
    ```

    Notice that the configuration `RDM_RECORDS_USER_FIXTURE_PASSWORDS` will take precedence over any password
    defined in the `users.yaml` file.

## Change password

To set or change the password for an existing user, create a new shell with `pipenv run invenio shell` and run:

```python
from flask_security.utils import hash_password
from invenio_accounts.proxies import current_datastore
from invenio_db import db

user = current_datastore.get_user("admin@inveniosoftware.org")
user.password = hash_password("my new psw")
current_datastore.activate_user(user)
db.session.commit()
```

## Create users programmatically

You might need to add users or modify their permissions after the initial user vocabulary has been loaded. You can achieve this using the InvenioRDM command-line interface.

Use the invenio users create command. The `--active` flag ensures the user can log in immediately, and `--confirm` confirms their email address (assuming email verification is enabled by default).

```shell
pipenv run invenio users create email@domain.edu --password <password> --active --confirm
```

This will automatically confirm the account. If you prefer the user to verify their email address themselves, omit the `--confirm` parameter:

## Create and assign roles

Roles are powerful mechanisms for managing permissions and granting access rights to users within InvenioRDM. They define what actions users can perform in the system. Users can hold multiple roles, and you can assign roles at different levels.

To create a new role and assign it to a user, use the following commands:

```shell
# Create a new role
invenio roles create <role-name>

# Assign role to a user
invenio roles add user@example.org <role-name>
```

InvenioRDM pre-defines various `actions` that provide flexible access authorization. You can assign these actions directly to users or to roles.

### Grant access to the administration panel

To give an account access the Administration panel, you need to assign the `administration-access` action to a user or to a role.

```shell
invenio access allow administration-access user <e-mail>
```

Or, you can create a role for the action, and then assign the role to multiple users:

```shell
invenio roles create administration
invenio access allow administration-access role administration
```

### Grant superuser rights

To grant a user account superuser rights, allowing them to access anything and perform any action within the system, assign the `superuser-access` action:

```shell
invenio access allow superuser-access user <e-mail>
```

## Confirm user

Only confirmed accounts can log in to InvenioRDM. You can confirm an account automatically upon creation using the `--confirm` parameter.

Alternatively you can confirm an account programmatically by opening a new shell using `pipenv run invenio shell` and
running:

```python
from flask_security.confirmable import confirm_user
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_users_resources.services.users.tasks import reindex_users

user = current_datastore.get_user("admin@inveniosoftware.org")
confirm_user(user)
db.session.commit()
reindex_users([user.id])
```
