# Users

Users are not a vocabulary *per se*, but they are loaded in the same fashion,
through the application data folder.

This file contains a list of users to create, and is stored in the root of the
`app_data` folder.

```
app_data/
└── users.yaml
```

If the file is provided but it is empty, no default user is created. If the
file is not provided, InvenioRDM creates an admin user with email
`admin@inveniosoftware.org` (and a random password).

The content of the file is as follows:

```yaml
<email>:
  active: <bool>
  password: <string>
  roles: <array of strings>
  allow: <array of strings>
```

- `<email>` : Email of the user.
- `active` : Is the user active or not.
- `password` : Their password. If empty, a random one is generated.
- `roles` : Array of roles the user has. The roles must already be present in the DB.
- `allow` : Array of action needs the user has.

InvenioRDM creates a default admin user with an inveniosoftware.org email; you
probably want to change that too. In this section, we outline how to customize
the data your instance uses.