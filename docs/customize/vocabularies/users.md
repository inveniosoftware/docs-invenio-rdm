# Users

Users are not a vocabulary *per se*, but they are loaded in the same fashion,
through the application data folder.

The file `users.yaml` contains a list of users to create, and is stored in the
root of the `app_data` folder.

```
app_data/
└── users.yaml
```

The content of the file is as follows:

```yaml
#list of users:
-  email: <string>
   active: <bool>
   password: <string>
   roles: <array of strings>
   allow: <array of strings>
```

- `email` : Email of the user.
- `active` : Is the user active or not.
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
