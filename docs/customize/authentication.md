# Authentication

!!! warning "Work in progress"
    This section has not yet been written.


## Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source solution for identity management
that can be used for single sign-on endpoints.


### Configuration of Keycloak in Invenio RDM

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
    base_url="https://localhost:4430", realm="invenio-realm"
)

OAUTHCLIENT_KEYCLOAK_REALM_URL = helper.realm_url
OAUTHCLIENT_KEYCLOAK_USER_INFO_URL = helper.user_info_url
OAUTHCLIENT_KEYCLOAK_REMOTE_APP = helper.remote_app()
OAUTHCLIENT_KEYCLOAK_REMOTE_REST_APP = helper.remote_rest_app()
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


### Tweaking the Generated Configuration

The `KeycloakSettingsHelper` is only there to make the configuration easier,
since the base URL and realm are used several times in the `remote_app` dictionary.
In case you need more fine-grained control over some of the values in the configuration,
you can of course change them.

Here is what the concrete configuration dictionaries generated as above look like:

```python
>>> helper.remote_app()
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
keycloak_remote_app = helper.remote_app()

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
