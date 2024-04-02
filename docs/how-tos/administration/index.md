# Accessing the Administration Panel

The following detailing the administration panel setup, how to add users and its interface and usage.

## Prerequisites

To access the Administration Panel, users must be logged in with an administrator role. The admin role is key to performing administrative tasks and is assigned from the instance's owners.

## Setup

Setting up access to the Administration Panel involves configuring the instance, creating roles, allowing these roles, and assigning them to users by instance's owners.

### Configuration

Firstly, ensure that the Administration Panel is enabled in your instance by adding the following configuration in `invendio.cfg`:

```python
USERS_RESOURCES_ADMINISTRATION_ENABLED = True
```

### Creating and Allowing Roles

Execute the following commands to create the necessary roles and permissions:

```shell
# Create and allow the roles once (usually done in the instance setup)
invenio roles create administration-moderation
invenio roles create administration

invenio access allow administration-moderation role administration-moderation
invenio access allow administration-access role administration
invenio access allow superuser-access role administration
```

### Assigning Roles to Users

To grant a user access to the Administration Panel, assign the administration role:

```shell
# allow the user to access the administration panel
invenio roles add user@demo.org administration
```

You can assign the moderation role to a admin if you want to allow access the users moderation panel:

```shell
# allow the user to access the moderation tab
invenio roles add user@demo.org administration-moderation
```

replace `user@demo.org` with the email of the user you want to give access to the administration panel.

## More Information

You can find more information about the Administration Panel in the following sections:

- [Architecture](../../develop/topics/administration_panel.md/#administration-panel)

- [References](../../reference/administration_reference.md/#administration-reference-guide)
