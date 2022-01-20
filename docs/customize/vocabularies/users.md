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

If the file is not provided, InvenioRDM creates an admin user with the email
`admin@inveniosoftware.org` (and a random password). If the file is provided
but is empty, no default user is created.
