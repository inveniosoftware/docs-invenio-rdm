# Authentication

InvenioRDM supports local authentication only, integration with your institutional authentication
system only or both at the same time.


## Local Authentication

By default, it is only the only authentication system enabled. Users can create a new account using the
registration form and activate their account after the email confirmation.

You can disable local authentication by setting in `invenio.cfg`:

```python
ACCOUNTS_LOCAL_LOGIN_ENABLED = False  # allow/deny users to login with a local account
```

In case that local logins are disabled, it also makes sense to disable the possibilities to register
new local accounts and change/recover passwords for local accounts:

```python
# login-related configuration items from Flask-Security
SECURITY_REGISTERABLE = False  # allow/deny new users to register locally
SECURITY_RECOVERABLE = False  # allow/deny resetting the local account's password
SECURITY_CHANGEABLE = False  # allow/deny changing passwords for local accounts
```

*Note:* Please make sure that your configuration is consistent!
While *some* clearly inconsistent configurations (e.g. having `SECURITY_RECOVERABLE=True`
and at the same time `ACCOUNTS_LOCAL_LOGIN_ENABLED=False`) trigger a warning at the time of
initialization, other inconsistent combinations may be accepted silently and ultimately
result in unexpected behavior and weird user experience.


## OAuth

In addition to local accounts, Invenio RDM offers the possibilty to integrate external
[OAuth 2](https://oauth.net/2/) / [OpenID Connect](https://openid.net/connect/)
authentication services via the
[Invenio-OAuthClient](https://invenio-oauthclient.readthedocs.io/en/latest/) module.


### Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source solution for identity management
that can be used for single sign-on endpoints.
It can be integrated in Invenio RDM as follows:


#### Configuration of Keycloak in InvenioRDM

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


#### Tweaking Keycloak Configuration

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
    "precedence_mask": {"email": True, "profile": {"username": False, "full_name": False}},
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

*Note:* The `precedence_mask` dictates for which fields of newly registered accounts
the `user_info` provided by the external authentication service should take precedence
over any user input.
This can be relevant for security considerations - for more information, see
[later sections](#on-the-precedence-mask).

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


#### Multiple Keycloak Authentication Providers

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


### General OAuth Configuration

In case that local login is disabled and there is exactly one OAuthClient remote app defined, the login screen
from InvenioRDM may seem a bit redundant.  
*Good news:* It can be skipped, having the login button redirect directly to the external login service:

```python
OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True
```

Also, it may be desirable to have the external authentication services act as the source
of truth for the users' profiles.
If so, the users can be prevented from updating their own user profiles by making them read-only:

```python
USERPROFILES_READ_ONLY = True
```


#### Customizing the Registration Form

Whenever a new users logs in to Invenio RDM via an external account for the first time,
a local account has to be created and linked to the external account.
Sometimes it is desirable to have this happen automatically behind the scenes, and
just populate the new account with the `user_info` provided by the external authentication
service.
At other times, it may be desirable to let users have the final say about their account's
details during sign-up.
Invenio RDM provides a mechanism to customize registration forms for external accounts
via the `OAUTHCLIENT_SIGNUP_FORM` configuration variable.

The following example configuration creates different registration forms for different
external services.
All of them have an extra checkbox for accepting the system's terms and conditions
which is mandatory to complete the registration:

```python
from invenio_userprofiles.forms import ProfileForm
from wtforms import BooleanField, validators, FormField
from werkzeug.local import LocalProxy
from flask import current_app, url_for

_security = LocalProxy(lambda: current_app.extensions['security'])

terms_of_use_url=url_for("static", filename=("documents/terms-of-use.pdf"))
terms_of_use_text = f"Accept the <a href='{terms_of_use_url}' target='_blank'>terms and conditions</a>"

def my_registration_form(*args, **kwargs):
    current_remote_app = kwargs.get("oauth_remote_app", "").lower()
    if current_remote_app != "orcid":
        class DefaultRegistrationForm(_security.confirm_register_form):
            email = None  # remove the email field
            password = None  # also remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None
            submit = None  # defined in the template
            terms_of_use = BooleanField(terms_of_use_text, [validators.required()])
        return DefaultRegistrationForm(*args, **kwargs)
    else:
        # orcid doesn't provide an email address, so we have to ask the user for that
        class OrcidRegistrationForm(_security.confirm_register_form):
            password = None  # remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None
            submit = None  # defined in the template
            terms_of_use = BooleanField(terms_of_use_text, [validators.required()])
        return OrcidRegistrationForm(*args, **kwargs)

OAUTHCLIENT_SIGNUP_FORM = my_registration_form
```


##### On the Precedence Mask

The details for the new account can be either taken from user input (as provided via
the registration form), or the `user_info` information provided by the external service.
In some cases it is preferrable to use the service's suggested values (if available)
rather than the user's arbitrary input (e.g. the email address, since this is used
in the internal mechanism for matching up previously unknown external accounts with
local accounts).
The set of fields for which the external service's `user_info` should be preferred
over user input (or vice versa) can be specified in each remote app's `precedence_mask`
configuration property.
Properties marked with `True` (or omitted from) in the precedence mask will be taken
from the `user_info` if available, while properties marked with `False` will be taken
from the user input.


## Further Remarks

Additional relevant configuration items from `Flask-Security` include salt values for the calculation of various
hash values, the requirement for e-mail verification and collection of login statistics:

```python
SECURITY_CONFIRMABLE = False  # whether or not the e-mail address for local accounts should be verified
SECURITY_TRACKABLE = False  # activate/deactivate tracking of login statistics

SECURITY_PASSWORD_SALT = "<SOME.GENERATED.SALT>"
SECURITY_CONFIRM_SALT = "<SOME.GENERATED.SALT>"
SECURITY_RESET_SALT = "<SOME.GENERATED.SALT>"
SECURITY_LOGIN_SALT = "<SOME.GENERATED.SALT>"
SECURITY_CHANGE_SALT = "<SOME.GENERATED.SALT>"
SECURITY_REMEMBER_SALT = "<SOME.GENERATED.SALT>"
```

Additional security-related configuration items can be found in the
[documentation for Flask-Security](https://flask-security.readthedocs.io/en/latest/configuration.html).
