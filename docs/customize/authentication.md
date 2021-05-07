# Authentication

InvenioRDM supports local authentication only, integration with your institutional authentication
system only or both at the same time.

## Local authentication

By default, it is only the only authentication system enabled. Users can create a new account using the
registration form and activate their account after the email confirmation.

You can disable local authentication by setting in `invenio.cfg`:

```python
ACCOUNTS_LOCAL_LOGIN_ENABLED = False
```

!!! warning "Work in progress"
    This section has not yet been written.


## OAuth

!!! warning "Work in progress"
    This section has not yet been written.

## Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source solution for identity management
that can be used for single sign-on endpoints.

### Configuration of Keycloak in InvenioRDM

What you need to know:
* The base URL (including port) of the Keycloak instance
* Information about the client, as configured in Keycloak:
    * Its realm
    * The client ID
    * The client secret
    * The target audience of Keycloak's JWTs (probably the same as the client ID)

*Note:* The client in Keycloak must have its access type set to *confidential*, and
use the client authenticator mechanism *client ID and secret*.

This information can be included in your `invenio.cfg` like so:

```python
from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper

helper = KeycloakSettingsHelper(
    title="Keycloak",
    description="Keycloak Authentication Service",
    base_url="https://localhost:4430",
    realm="invenio-realm"
)

OAUTHCLIENT_KEYCLOAK_REALM_URL = helper.realm_url
OAUTHCLIENT_KEYCLOAK_USER_INFO_URL = helper.user_info_url
OAUTHCLIENT_KEYCLOAK_VERIFY_EXP = True  # whether to verify the expiration date of tokens
OAUTHCLIENT_KEYCLOAK_VERIFY_AUD = True  # whether to verify the audience tag for tokens
OAUTHCLIENT_KEYCLOAK_AUD = "<YOUR.AUDIENCE>"  # probably the same as the client ID

OAUTHCLIENT_REMOTE_APPS = {
    "keycloak": OAUTHCLIENT_KEYCLOAK_REMOTE_APP,
    # additional remote apps, if desired...
}

KEYCLOAK_APP_CREDENTIALS = {
    "consumer_key": "<YOUR.CLIENT.ID>",
    "consumer_secret": "<YOUR.CLIENT.CREDENTIALS.SECRET>",
}
```

### Tweaking Keycloak configuration

The `KeycloakSettingsHelper` is only there to make the configuration easier,
since the base URL and realm are used several times in the `remote_app` dictionary.
In case you need more fine-grained control over some of the values in the configuration,
you can of course change them.

Here is what the concrete configuration dictionaries generated as above look like:

```python
>>> helper.remote_app
{
    "title": "Keycloak",
    "description": "Keycloak Authentication Service",
    "icon": "",
    "authorized_handler": "invenio_oauthclient.handlers:authorized_signup_handler",
    "disconnect_handler": "invenio_oauthclient.contrib.keycloak.handlers:disconnect_handler",
    "signup_handler": {
        "info": "invenio_oauthclient.contrib.keycloak.handlers:info_handler",
        "setup": "invenio_oauthclient.contrib.keycloak.handlers:setup_handler",
        "view": "invenio_oauthclient.handlers:signup_handler"
    },
    "params": {
        "base_url": "https://localhost:4430",
        "request_token_params": {"scope": "openid"},
        "request_token_url": None,
        "access_token_url": "https://localhost:4430/auth/realms/invenio-realm/protocol/openid-connect/token",
        "access_token_method": "POST",
        "authorize_url": "https://localhost:4430/auth/realms/invenio-realm/protocol/openid-connect/auth",
        "app_key": "KEYCLOAK_APP_CREDENTIALS"
    }
}

>>> helper.realm_url
"https://localhost:4430/auth/realms/invenio-realm"

>>> helper.user_info_url
"https://localhost:4430/auth/realms/invenio-realm/protocol/openid-connect/userinfo"
```

*Note:* The value `remote_app["params"]["app_key"]` stores the name of the configuration
variable holding the Keycloak client credentials.
In case that multiple Keycloak remote apps should be registered, this variable has to be
renamed for each of the remote apps.
To rename the configuration variable (e.g. from `KEYCLOAK_APP_CREDENTIALS` to
`OAUTHCLIENT_KEYCLOAK_APP_CREDENTIALS`), this value has to be updated as well.

Since `invenio.cfg` is a Python module, the values can be manipulated programmatically:

```python
keycloak_remote_app = helper.remote_app

# change the title of the remote app
keycloak_remote_app["title"] = "Our Awesome Keycloak!"

# change the name of the variable holding the credentials
remote_app["params"]["app_key"] = "OAUTHCLIENT_KEYCLOAK_APP_CREDENTIALS"
OAUTHCLIENT_KEYCLOAK_APP_CREDENTIALS = {
    "consumer_key": "<YOUR.CLIENT.ID>",
    "consumer_secret": "<YOUR.CLIENT.CREDENTIALS.SECRET>",
}

# update the remote apps configuration
OAUTHCLIENT_REMOTE_APPS["keycloak"] = keycloak_remote_app
```

### Multiple Keycloak authentication providers

You might have the need to integrate multiple Keycloak authentication providers at the same time, to allow
users to login with one or the other.

You can define multiple Keycloak apps in your `invenio.cfg`, by namespacing:

```python
from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper

foo = KeycloakSettingsHelper(
    title="Foo provider",
    description="Keycloak Authentication foo provider",
    base_url="https://foo.com:4430",
    realm="foo-realm"
    app_key="FOO_KEYCLOAK_APP_CREDENTIALS"
)

bar = KeycloakSettingsHelper(
    title="Bar provider",
    description="Keycloak Authentication bar provider",
    base_url="https://bar.com:4430",
    realm="bar-realm"
    app_key="BAR_KEYCLOAK_APP_CREDENTIALS"
)

OAUTHCLIENT_REMOTE_APPS = {
    "foo_keycloak": foo.remote_app,
    "bar_keycloak": bar.remote_app,
}

OAUTHCLIENT_FOO_KEYCLOAK_REALM_URL = foo.realm_url
OAUTHCLIENT_FOO_KEYCLOAK_USER_INFO_URL = foo.user_info_url
OAUTHCLIENT_FOO_KEYCLOAK_VERIFY_EXP = True
OAUTHCLIENT_FOO_KEYCLOAK_VERIFY_AUD = True
OAUTHCLIENT_FOO_KEYCLOAK_AUD = "<FOO.AUDIENCE>"

OAUTHCLIENT_BAR_KEYCLOAK_REALM_URL = bar.realm_url
OAUTHCLIENT_BAR_KEYCLOAK_USER_INFO_URL = bar.user_info_url
OAUTHCLIENT_BAR_KEYCLOAK_VERIFY_EXP = False
OAUTHCLIENT_BAR_KEYCLOAK_VERIFY_AUD = True
OAUTHCLIENT_BAR_KEYCLOAK_AUD = "<BAR.AUDIENCE>"

FOO_KEYCLOAK_APP_CREDENTIALS = {
    "consumer_key": "<FOO.CLIENT.ID>",
    "consumer_secret": "<FOO.CLIENT.CREDENTIALS.SECRET>",
}

BAR_KEYCLOAK_APP_CREDENTIALS = {
    "consumer_key": "<BAR.CLIENT.ID>",
    "consumer_secret": "<BAR.CLIENT.CREDENTIALS.SECRET>",
}
```

!!! warning "Naming convention"
    Notice how the `app_key` param must match with the name of the config `<APP_KEY>_APP_CREDENTIALS`, uppercase,
    and the name of the apps in the config `OAUTHCLIENT_REMOTE_APPS` (`foo_keycloak`, `bar_keycloak`) must match
    with the related config vars `OAUTHCLIENT_FOO_KEYCLOAK_*` and `OAUTHCLIENT_BAR_KEYCLOAK_*`, uppercase.
