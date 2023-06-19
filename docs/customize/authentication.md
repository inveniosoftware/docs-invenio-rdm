# Authentication

InvenioRDM supports local authentication only, integration with your institutional authentication
system only (e.g. OAuth, SAML, Single Sign-on) or both at the same time.

## Local Authentication

By default, only the local authentication system is enabled. Users can create a new account using the
registration form and activate their account after the email confirmation. These defaults are set
in ``invenio.cfg``:

```python
ACCOUNTS_LOCAL_LOGIN_ENABLED = True  # enable local login
SECURITY_REGISTERABLE = True  # local login: allow users to register
SECURITY_RECOVERABLE = True  # local login: allow users to reset the password
SECURITY_CHANGEABLE = True  # local login: allow users to change password
SECURITY_CONFIRMABLE = True  # require users to confirm their e-mail address
```

### Disabling local authentication

You can disable local authentication by modifying the setting in `invenio.cfg`:

```python
ACCOUNTS_LOCAL_LOGIN_ENABLED = False  # disable local login
```

You typically disable local authentication when you want authentication to be handled by an external provider.
As such, when local login is disabled, **it is recommended** to disable local account registration and password
change/recovery:

```python
SECURITY_REGISTERABLE = False  # deny local registration of new users
SECURITY_RECOVERABLE = False  # deny resetting the local account's password
SECURITY_CHANGEABLE = False  # deny changing passwords for local accounts
```

This way the external provider handles account management. `SECURITY_CONFIRMABLE` is kept `True` to check
that the user can be reached via a valid email.

!!! warning "Make sure that your configuration is consistent!"
    While *some* clearly inconsistent configurations (e.g. having `SECURITY_REGISTERABLE=True`
    and at the same time `ACCOUNTS_LOCAL_LOGIN_ENABLED=False`) will trigger a console **warning**
    when running the Invenio webserver, other inconsistent combinations may be silently
    accepted and ultimately result in unexpected behaviors.

## External authentication

InvenioRDM supports external authentication out-of-the-box, such as OAuth. SAML authentication
can also be experimentally enabled.

Note that the redirect url (or _authorized_) has the format `https://<CFG_SITE_URL>/oauth/authorized/<contrib>/`,
where contrib can be _orcid_, _cern_, _github_, etc.

### OAuth

In addition to local accounts, InvenioRDM offers the possibility to integrate external
[OAuth 2](https://oauth.net/2/) / [OpenID Connect](https://openid.net/connect/)
authentication services via the
[Invenio-OAuthClient](https://invenio-oauthclient.readthedocs.io/en/latest/) module.

#### ORCID

After having registered a new client application in the ORCID website and having set as `authorized` URL
`https://<CFG_SITE_URL>/oauth/authorized/orcid/`, you can enable ORCID login in InvenioRDM by enabling
the plugin and configuring key and secret. In your `invenio.cfg`:

```python
from invenio_oauthclient.contrib import orcid

OAUTHCLIENT_REMOTE_APPS = dict(
    orcid=orcid.REMOTE_APP,
)

ORCID_APP_CREDENTIALS = dict(
    consumer_key="<my-key>",
    consumer_secret="<my-secret>",
)
```

You can also test ORCID login using the ORCID sandbox environment.
See the
plugin [documentation](https://invenio-oauthclient.readthedocs.io/en/latest/usage.html#module-invenio_oauthclient.contrib.orcid)
for more information.

#### Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source solution for identity management
that can be used for single sign-on endpoints.

##### Configuration

Information required to configure the InvenioRDM instance:

* The base URL (including port) of the Keycloak server.
* Information about the client, as configured in Keycloak:
    * Its realm.
    * The client ID.
    * The client secret.
    * The target audience of Keycloak's JWTs (probably the same as the client ID).

!!! note
    The client configuration in Keycloak server must have its access type set
    to *confidential* and use the client authenticator mechanism *client ID and secret*.

In your `invenio.cfg`:

```python
from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper

helper = KeycloakSettingsHelper(
    title="Keycloak",
    description="Keycloak Authentication Service",
    base_url="https://myserver.com:4430",
    realm="my-realm"
)

OAUTHCLIENT_KEYCLOAK_REALM_URL = helper.realm_url
OAUTHCLIENT_KEYCLOAK_USER_INFO_URL = helper.user_info_url
OAUTHCLIENT_KEYCLOAK_VERIFY_EXP = True  # whether to verify the expiration date of tokens
OAUTHCLIENT_KEYCLOAK_VERIFY_AUD = True  # whether to verify the audience tag for tokens
OAUTHCLIENT_KEYCLOAK_AUD = "<YOUR.AUDIENCE>"  # probably the same as the client ID

OAUTHCLIENT_REMOTE_APPS = {
    "keycloak": helper.remote_app,
}

KEYCLOAK_APP_CREDENTIALS = {
    "consumer_key": "<YOUR.CLIENT.ID>",
    "consumer_secret": "<YOUR.CLIENT.CREDENTIALS.SECRET>",
}
```

##### Tweaking configuration

The `KeycloakSettingsHelper` is only there to make the configuration easier,
since the base URL and realm are used several times in the `remote_app` dictionary.
You can change many other settings of the Keycloak configuration in case you need
more fine-grained control.

Here is what the full configuration looks like:

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
        "base_url": "https://myserver.com:4430",
        "request_token_params": {"scope": "openid"},
        "request_token_url": None,
        "access_token_url": "https://myserver.com:4430/auth/realms/my-realm/protocol/openid-connect/token",
        "access_token_method": "POST",
        "authorize_url": "https://myserver.com:4430/auth/realms/my-realm/protocol/openid-connect/auth",
        "app_key": "KEYCLOAK_APP_CREDENTIALS"
    }
}

>>> helper.realm_url
"https://myserver.com:4430/auth/realms/my-realm"

>>> helper.user_info_url
"https://myserver.com:4430/auth/realms/my-realm/protocol/openid-connect/userinfo"
```

!!! note
    The `precedence_mask` dictates which information about the user (name, email, etc.)
    provided by authentication server should take precedence over any user input.
    For more information, see [the related section](#on-the-precedence-mask).

You can modify default configuration directly in your `invenio.cfg`:

```python
keycloak_remote_app = helper.remote_app

# change the title that will be shown in the login button "Login with My institute"
keycloak_remote_app["title"] = "My institute"

# change the name of the variable holding the credentials
keycloak_remote_app["params"]["app_key"] = "OAUTHCLIENT_ANOTHER_NAME_APP_CREDENTIALS"
OAUTHCLIENT_ANOTHER_NAME_APP_CREDENTIALS = {
    "consumer_key": "<YOUR.CLIENT.ID>",
    "consumer_secret": "<YOUR.CLIENT.CREDENTIALS.SECRET>",
}

# update the remote apps configuration
OAUTHCLIENT_REMOTE_APPS["keycloak"] = keycloak_remote_app
```

##### Multiple Keycloak authentication providers

You might have the need to integrate multiple Keycloak authentication providers at the same time, to allow
users to login with one or the other. You can "namespace" each remote application using a different
value for the parameter `app_key`. In your `invenio.cfg`:

```python
from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper

foo = KeycloakSettingsHelper(
    title="Foo provider",
    description="Keycloak Authentication foo provider",
    base_url="https://foo.com:4430",
    realm="foo-realm",
    app_key="FOO_KEYCLOAK_APP_CREDENTIALS"
)

bar = KeycloakSettingsHelper(
    title="Bar provider",
    description="Keycloak Authentication bar provider",
    base_url="https://bar.com:4430",
    realm="bar-realm",
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

#### OpenAIRE AAI

Register a new application with OpenAIRE, by sending an email to <aai@openaire.eu>, with the following information:

* Client ID for your application (e.g. ``my-app``).
* One or more *Redirect URI*s pointing to ``https://<host>/oauth/authorized/openaire_aai/`` (
  e.g. ``https://localhost:5000/oauth/authorized/openaire_aai/``).
* User claim scopes ``openid profile email orcid``.
* One or more of the OpenID Connect/OAuth2 grant types: Authorization Code, Token Exchange, Device Code.
* Optionally, you can request to also register an application for the OpenAIRE AAI sandbox instance for testing.

After registering your application, you can enable OpenAIRE login in InvenioRDM by enabling the plugin and configuring
the key and secret. In your `invenio.cfg`:

```python
from invenio_oauthclient.contrib import openaire_aai

OAUTHCLIENT_REMOTE_APPS = dict(
    openaire_aai=openaire_aai.REMOTE_APP,
)

OPENAIRE_APP_CREDENTIALS = dict(
    consumer_key="changeme",
    consumer_secret="changeme",
)
```

In case you want use the sandbox environment, use ``openaire_aai.REMOTE_SANDBOX_APP`` instead
of ``openaire_aai.REMOTE_APP``.

### Login automatic redirection

When local login is disabled and there is exactly one OAuthClient remote app defined, the login page
can be skipped and the user can be redirected directly to the external authentication provider.
In your `invenio.cfg`:

```python
from invenio_oauthclient.views.client import auto_redirect_login

ACCOUNTS_LOGIN_VIEW_FUNCTION = auto_redirect_login
OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True
```

This automatic redirection will not work, even if configured as above, if local login is enabled or you
have configured multiple remote applications.

### User profile update

You might want to disable the update of the user profile (email, full name, etc.) when only external
authentication is enabled.
You can set the user profile form as read-only by changing in your `invenio.cfg`:

```python
USERPROFILES_READ_ONLY = True
```

### Auto-confirm user

*Introduced in InvenioRDM v11*

By default, users who login using an external authentication provider are `confirmed` and the e-mail confirmation
is not sent any more.

The only exception is the ORCID OAuth plugin: the user e-mail cannot be retrieved by this provider
and the user must provide it when registering for the first time.
In this case, the registration follows the classic flow, with e-mail confirmation.

You can modify this behavior per plugin:

```diff
_keycloak_helper = KeycloakSettingsHelper(
    title="CERN",
    description="CERN SSO authentication",
    ...
+    signup_options=dict(
+        auto_confirm=True,
+        send_register_msg=False,
+    ),
)
```

### On the precedence mask

On first user login after external authentication flow, the user information are fetched
from the authentication provider or they might be input by the user via a
[custom registration form](#custom-user-registration-form).

You can enforce what user information should be taken from the server and cannot be overridden
by the user during registration, so that you are sure what information to trust.
In your OAuth application, you can fine tune the `precedence_mask`:

```python
remote_app["precedence_mask"] = {"email": True, "profile": {"username": False, "full_name": False}}
```

Properties marked with `True` (or omitted) in the precedence mask will be taken
from the authentication server user information payload if available, while properties marked
with `False` will be taken from the user input in the registration form.

### Defining post logout url

By default, upon logging out, the application will disconnect you only from itself. However, if you logged in through an external provider, logging out from the application will not automatically log you out from that provider. To address this, you can define a `logout_url` when setting up the remote apps:

```diff
_keycloak_helper = KeycloakSettingsHelper(
    title="CERN",
    description="CERN SSO authentication",
    ...
+   logout_url="your_app/logout",
    ),
)
```

After setting the `logout_url`, it is necessary to include the following configuration variable:

```python
SECURITY_POST_LOGOUT_VIEW = "/oauth/logout"
"""Required by invenio-oauthclient to be able to set logout urls for the remote apps."""
```

This will redirect to the appropriate `logout_url` for each of the enabled remotes in the instance.

## Security

For increased security, you should define the following in your `invenio.cfg`:

```python
SECURITY_CONFIRMABLE = True  # enable e-mail address confirmation for local login
SECURITY_TRACKABLE = True  # enable tracking of basic user login statistics

SECURITY_PASSWORD_SALT = "..put a long random value here.."
SECURITY_CONFIRM_SALT = "..put a long random value here.."
SECURITY_RESET_SALT = "..put a long random value here.."
SECURITY_LOGIN_SALT = "..put a long random value here.."
SECURITY_CHANGE_SALT = "..put a long random value here.."
SECURITY_REMEMBER_SALT = "..put a long random value here.."
```

Additional configuration items for security, sending and customising account registration-related emails, etc. can be found in the
[documentation for Flask-Security](https://flask-security.readthedocs.io/en/latest/configuration.html).

You can change the default duration (31 days) of the logged in user session (the session cookie expiration).
This is particularly useful when configuring InvenioRDM with external authentication only and you want to
have the same session duration as the external authentication provider.

In your `invenio.cfg`:

```python
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
```

## Advanced integrations

### Custom login page

You can customize the login page template to display different information or
change its look and feel.

Start from an existing template:

* If you have local login only, copy the
  folder [templates/semantic-ui](https://github.com/inveniosoftware/invenio-accounts/tree/master/invenio_accounts/templates/semantic-ui)
  from `invenio-accounts`.
* If you have external authentication, copy the
  folder [templates/semantic-ui](https://github.com/inveniosoftware/invenio-oauthclient/tree/master/invenio_oauthclient/templates/semantic-ui)
  from `invenio-oauthclient`.

Then, open the `templates` folder in `my-site` (your instance) and paste it there. Inside the
`invenio-accounts`/`invenio-oauthclient` folder, keep only the template file that you want to customize.

Edit the Jinja template as you need.

For more information, see the guide [style other pages](look-and-feel/templates.md).

### Custom user registration form

Whenever a new user logs in to InvenioRDM with external authentication for the first time,
Invenio will create a local account associated with the external account.

The local account user information, such as e-mail, username and full name are normally
fetched when authenticating and automatically filled in. In case of ORCID login, the
user e-mail cannot be retrieved when authenticating and a registration form will be
prompted to the user asking to fill in the e-mail.

You can customize such behavior and allow users to modify the information coming from
the authentication server or require extra user input (e.g. require the user to accept
website terms and conditions).

The following example configuration creates different registration forms for different
external authentication providers.
All of them have an extra checkbox for accepting the website's terms and conditions,
which is mandatory to complete the registration:

``my_package/registration_form.py``:

```python
from invenio_oauthclient.utils import create_registrationform
from invenio_userprofiles.forms import ProfileForm
from wtforms import BooleanField, validators, FormField
from werkzeug.local import LocalProxy
from flask import current_app, url_for
from markupsafe import Markup

_security = LocalProxy(lambda: current_app.extensions['security'])


def my_registration_form(*args, **kwargs):
    # create a link to a PDF file containing the terms and conditions
    # the PDF file is located in the `static/documents` folder.
    terms_of_use_url = url_for("static", filename=("documents/terms-of-use.pdf"))
    terms_of_use_text = Markup(f"Accept the <a href='{terms_of_use_url}' target='_blank'>terms and conditions</a>")
    current_remote_app = kwargs.get("oauth_remote_app")
    if not current_remote_app:
        # return default just in case something is wrong
        return create_registrationform(*args, **kwargs)
    # optionally, have different registration forms depending on the authentication
    # provider used by the user to login
    elif current_remote_app.name.lower() != "orcid":
        # show this form in case the user logged in with any method but ORCID
        class DefaultRegistrationForm(_security.confirm_register_form):
            email = None  # remove the email field
            password = None  # remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None  # remove the captcha
            submit = None  # remove submit btn, already defined in the template
            terms_of_use = BooleanField(terms_of_use_text, [validators.required()])  # add the new field

        return DefaultRegistrationForm(*args, **kwargs)
    else:
        # ORCID does not provide the user e-mail address, it must be input by the user.
        # the email field comes from `confirm_register_form` upper class.
        class OrcidRegistrationForm(_security.confirm_register_form):
            password = None  # remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None  # remove the captcha
            submit = None  # remove submit btn, already defined in the template
            terms_of_use = BooleanField(terms_of_use_text, [validators.required()])  # add the new field

        return OrcidRegistrationForm(*args, **kwargs)
```

``invenio.cfg``:

```python
from my_package.registration_form import my_registration_form

# use the custom form function
OAUTHCLIENT_SIGNUP_FORM = my_registration_form
```

### Custom user info

*Introduced in InvenioRDM v11*

You can customize how each OAuth plugin will fetch the user information on login, and what
fields should be kept or how they should be serialized.

You can customize the function that will be called to fetch the user information:

```python
def info_handler(remote, resp):
    """Retrieve remote account information.

    :param remote: The remote application.
    :param resp: The response of the `authorized` endpoint.
    :returns: A dictionary with the user information.
    """
    user_info = ... fetch user info ...
    return custom_info_serializer(user_info)

_keycloak_helper = KeycloakSettingsHelper(...)

handlers = _keycloak_helper.get_handlers()
handlers["signup_handler"]["info"] = custom_info_serializer
```

You can customize the function that will be called to serialize the user information:

```python
def custom_info_serializer(remote, resp, user_info):
    """Serialize the account info response object.

    :param remote: The remote application.
    :param resp: The response of the `authorized` endpoint.
    :param user_info: The response of the `user info` endpoint.
    :returns: A dictionary with serialized user information.
    """
    return {
        "user": {
            "active": True,
            "email": user_info["email"],
            "profile": {
                "full_name": user_info["name"],
                "username": user_info["preferred_username"],
            },
            "prefs": {
                "visibility": "restricted",
                "email_visibility": "restricted",
            },
        },
        "external_id": user_info["upn"],
        "external_method": remote.name,
    }

_keycloak_helper = KeycloakSettingsHelper(...)

handlers = _keycloak_helper.get_handlers()
handlers["signup_handler"]["info_serializer"] = custom_info_serializer
```

!!! info "Mandatory external id"
    When customizing an info endpoint, it is mandatory for a field to provide an external ID. This field must be named `external_id`.


### New OAuth plugins

If you need to implement your own OAuth plugin to enable integration with your OAuth provider,
you can take advantage of the available OAuth helper class. You will need anyway to implement some
authentication handlers depending on your server authentication workflow. You can take a look
to existing implementations in [Invenio-OAuthClient](https://invenio-oauthclient.readthedocs.org).

In your `invenio.cfg`:

```python
from invenio_oauthclient.contrib.settings import OauthSettingsHelper


class MyOAuthSettingsHelper(OAuthSettingsHelper):
    def __init__():
        super().__init__(
            title="my plugin",
            description="a description",
            base_url="https://myserver.com/",
            app_key="MY_APP_CREDENTIALS",
            access_token_url="https://myserver.com/oauth/token",
            authorize_url="https://myserver.com/oauth/authorize",
        )

        def get_handlers(self):
            return dict(
                authorized_handler='invenio_oauthclient.handlers'
                                   ':authorized_signup_handler',
                disconnect_handler=my_disconnect_handler,
                signup_handler=dict(
                    info=my_account_info,
                    setup=my_account_setup,
                    view='invenio_oauthclient.handlers:signup_handler',
                )
            )

        def get_rest_handlers(self):
            return dict(
                authorized_handler='invenio_oauthclient.handlers.rest'
                                   ':authorized_signup_handler',
                disconnect_handler=my_disconnect_handler,
                signup_handler=dict(
                    info=my_account_info,
                    setup=my_account_setup,
                    view='invenio_oauthclient.handlers.rest:signup_handler',
                ),
                response_handler='invenio_oauthclient.handlers.rest'
                                 ':default_remote_response_handler',
                authorized_redirect_url='/',
                disconnect_redirect_url='/',
                signup_redirect_url='/',
                error_redirect_url='/'
            )

    )

    def my_disconnect_handler(...):
        ...

    def my_account_info(...):
        ...

    def my_account_setup(...):
        ...

    myOAuthHelper = MyOAuthSettingsHelper()

    OAUTHCLIENT_REMOTE_APPS = dict(
        myoauth=myOAuthHelper.remote_app,
    )

    MY_APP_CREDENTIALS = dict(
        consumer_key="<my-key>",
        consumer_secret="<my-secret>",
    )
```

### Allow/deny user login

When using external authentication, you might want to allow or deny user login base on some conditions.
For example, you might want to allow only users with e-mails from a specific domain `@mydomain.com`.

To implement such functionality, you will have to change the implementation of the `signup_handler.info` handler.
First, see how to implement a [new custom plugin](#new-oauth-plugins). You can also copy/paste an existing one.

Then, implement the `signup_handler.info` handler as the following (example taken from Keycloak plugin):

```python
from flask import flash


def account_info(remote, resp):
    user_info = get_user_info(remote, resp)
    email = user_info["email"].lower()
    if not email.endswith("@mydomain.com"):
        flash(_('You are not allowed to login on this website.'), category='danger')
        abort(401)
    else:
        # default implementation
        ...
```

### SAML integration

!!! warning
    While the SAML integration has been tested and should be working following the guide below, it might still need
    some further updates, in particular to make its configuration easier.

SAML stands for Security Assertion Markup Language. It is an XML-based open-standard for transferring identity
data between two parties: an identity provider (IdP) and a service provider (SP).

* **Identity Provider (IDP)**: Performs authentication and passes the user's identity and authorization level to the
  service provider.
* **Service Provider (SP)**: Trusts the identity provider and authorizes the given user to access the requested
  resource.

#### Prerequisites

* Make sure you have installed in your system:

  `libxml2-dev libxmlsec1-dev pkg-config`

* Make sure you have installed the required Invenio Python module:

    ```console
    cd my-site
    pipenv run pip install invenio-saml
    ```

#### Server information

List of information required to configure the InvenioRDM instance.

* SAML requires a x.509 cert to sign and encrypt elements like `NameID`, `Message`, `Assertion`, `Metadata`.

    * **sp.crt**: The public cert of the SP.
    * **sp.key**: The private key of the SP.

* **EntityID**: Identifier of the IdP entity  (must be a URI).
* **SSO(singleSignOnService)**: URL Target of the IdP where the Authentication Request Message will be sent.
* **SLO(singleLogoutService)**: URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout).
* **x509cert**: Public X.509 certificate of the IdP.
* **Attributes mapping**: IDP in Assertion of the SAML Response provides a dict with all the user data:

    *  For example, given the following SAML response:
    ```json
    {
        "cn": ["Jhon"],
        "sn": ["Doe"],
        "mail": ["john.doe@example.com"],
        "external_id": ["24546786764d"]
    }
    ```
    * You can create a mapping to the user account fields required by Invenio as the following:
    ```json
        "mappings": {
            "email": "mail",
            "name": "cn",
            "surname": "sn",
            "external_id": "external_id",
        },
    ```

#### Configuration

In your `invenio.cfg`:

```python
from invenio_saml.handlers import acs_handler_factory

SSO_SAML_DEFAULT_BLUEPRINT_PREFIX = '/saml'
"""Base URL for the extensions endpoint."""

SSO_SAML_DEFAULT_METADATA_ROUTE = '/metadata/<idp>'
"""URL route for the metadata request."""

SSO_SAML_DEFAULT_SSO_ROUTE = '/login/<idp>'
"""URL route for the SP login."""

SSO_SAML_DEFAULT_ACS_ROUTE = '/authorized/<idp>'
"""URL route to handle the IdP login request."""

SSO_SAML_DEFAULT_SLO_ROUTE = '/slo/<idp>'
"""URL route for the SP logout."""

SSO_SAML_DEFAULT_SLS_ROUTE = '/sls/<idp>'
"""URL route to handle the IdP logout request."""

SSO_SAML_IDPS = {

    # name your authentication provider
    'remote_app': {

        # Basic info
        "title": "SAML",
        "description": "SAML Authentication Service",
        "icon": "",

        # path to the file i.e. "./saml/sp.crt"
        'sp_cert_file': '<./SP_CERT_FILE>',

        # path to the file i.e. "./saml/sp.key"
        'sp_key_file': '<./SP_KEY_FILE>',

        'settings': {
            # If strict is True, then the Python Toolkit will reject unsigned
            # or unencrypted messages if it expects them to be signed or encrypted.
            # Also it will reject the messages if the SAML standard is not strictly
            # followed. Destination, NameId, Conditions ... are validated too.
            'strict': True,

            # Enable debug mode (outputs errors).
            'debug': True,

            # Service Provider Data that we are deploying.
            'sp': {

                # Specifies the constraints on the name identifier to be used to
                # represent the requested subject.
                # Take a look on https://github.com/onelogin/python-saml/blob/master/src/onelogin/saml2/constants.py
                # to see the NameIdFormat that are supported.
                'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
            },

            # Identity Provider Data that we want connected with our SP.
            'idp': {

                # Identifier of the IdP entity  (must be a URI)
                'entityId': '<IdP_Entity>',

                # SSO endpoint info of the IdP. (Authentication Request protocol)
                'singleSignOnService': {

                    # URL Target of the IdP where the Authentication Request Message
                    # will be sent.
                    'url': '<SSO_URL>',

                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    'binding':
                        'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                },

                # SLO endpoint info of the IdP.
                'singleLogoutService': {

                    # URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)
                    'url': '<SLS_URL>',

                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    'binding':
                        'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                },
                # Public X.509 certificate of the IdP
                'x509cert': '<X.509_oneliner>'
            },

            # Security settings
            # more on https://github.com/onelogin/python-saml
            'security': {
                'authnRequestsSigned': False,
                'failOnAuthnContextMismatch': False,
                'logoutRequestSigned': False,
                'logoutResponseSigned': False,
                'metadataCacheDuration': None,
                'metadataValidUntil': None,
                'nameIdEncrypted': False,
                'requestedAuthnContext': False,
                'requestedAuthnContextComparison': 'exact',
                'signMetadata': False,
                'signatureAlgorithm':
                    'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
                'wantAssertionsEncrypted': False,
                'wantAssertionsSigned': False,
                'wantAttributeStatement': False,
                'wantMessagesSigned': False,
                'wantNameId': True,
                'wantNameIdEncrypted': False,
                'digestAlgorithm':
                    'http://www.w3.org/2001/04/xmlenc#sha256'
            },
        },

        # Account Mapping
        "mappings": {
            "email": "<attribute_email>",
            "name": "<attribute_name>",
            "surname": "<attribute_surname>",
            "external_id": "<attribute_external_id>",
        },

        # Inject your remote_app to handler
        # Note: keep in mind the string should match
        # given name for authentication provider
        'acs_handler': acs_handler_factory('remote_app'),

        # Automatically set `confirmed_at` for users upon
        # registration, when using the default `acs_handler`
        'auto_confirm': False,
    }
}
```
#### Automatically confirm users
When using the default `acs_handler` for an authentication provider, users can be automatically confirmed upon registration by setting the `auto_confirm` attribute of a provider to `True` (default is `False`).
This will set the `confirmed_at` attribute of the user to the current time.

This can be done on a per provider basis, as not every provider may receive the same level of trust for a repository.

The `mappings` attributes are critical to getting your SAML configuration working correctly.  The values for `<attibute_email>`, `<attribute_name>`, `<attribute_surname>` and `<attribute_external_id>` are set in the `urn:oid` notation. If you are coming from an institution that uses the eduPerson as what is returned from your IdP you'll need to make those names into the `urn:oid` form. Example mapping of `urn:oasis` to `urn:oid` like those provided at [University of California](https://spaces.ais.ucla.edu/display/iamucladocs/Mapping+of+URN+Attributes+and+OID+Attributes) administrative information systems website may provide a clue to how your institution needs to map the SAML response from the IdP.

NOTE: In the above example the `<idp>` values do not need to be replaced. Invenio-RDM will map those internally.

##### Example configurations element

Here's an example mapping eduPerson elements to `urn:oid`. If you're not sure of your institutions mappings reach out to your IdP and search for "`eduPerson to `urn:oid`" and see what others have documented.

```
        "mappings": {
            # email mapped form eduPerson.mail
            "email": "urn:oid:0.9.2342.19200300.100.1.3",
            # name mapped from eduPerson.givenName
            "name": "urn:oid:2.5.4.42",
            # surname maps to eduPerson.sn
            "surname": "urn:oid:2.5.4.4",
            # external_id mapps to eduPerson.eduPersonPrincipalName
            # (e.g. jane.doe@example.edu)
	        "external_id": "urn:oid:1.3.6.1.4.1.5923.1.1.1.6",
        },

```


##### Troubleshooting SAML configuration

In setting up SAML integration you may run into several scenarios before you "get it right".

What are the InvenioRDM SP end points?
: In the example above the `SSO_SAML_IDPS` is a dictionary, the attributes are the names that will be used by InvenioRDM in the SAML interactions. In the example "remote_app" will be an end point, this is probably not ideal, if you have one IdP only you could just name that attribute "ipd", if you have several then a more descriptive attribute name might be warranted. 

SSO redirects work but Invenio shows 404 on return
: This can happen when the IdP is configured in InvenioRDM, the IdP has authorized your SP (the running InvenioRDM instance). If the user isn't actually "logged in" then you may also have trouble in your `mappings` element.

SSO redirects work, InvenioRDM returns a dashboard
: It is possible to have SAML/Shibboleth work from some users and not others. This maybe cause by an incorrect `mappings`. Double check that the values needed by InvenioRDM are getting correct responses, this can be done from checking your system logs for the running InvenioRDM instance.

SSO logout fails
: This could be as simple as correcting the `url` value in the `Idp`, `singleLogoutService` section. If ancient versions of SAML/Shibboleth did not support "logging out".


#### Show the login button

The last step is to enable the login template, provided by the SAML module, to display the new button
`Login with SAML`.
In your `invenio.cfg`:

```python
OAUTHCLIENT_LOGIN_USER_TEMPLATE = "invenio_saml/login_user.html"
```

#### Multiple SAML authentication providers

You might have the need to integrate multiple SAML authentication providers at the same time, to allow users to login
with one or the other.
You can define multiple SAML apps in your `invenio.cfg`:

```python
SSO_SAML_IDPS = {
    # First authentication provider
    "remote_app": {
        ....
        'settings': {
            ....
        },
        ....
        'acs_handler': acs_handler_factory('remote_app'),
        'auto_confirm': True,
    },
    # Second authentication provider
    "remote_app2": {
            ....
        'settings': {
            ....
        },
        ....
        'acs_handler': acs_handler_factory('remote_app2'),
        'auto_confirm': False,
    },
}
```

### Groups

A `group` is a set of users that can be managed in your organization, externally to InvenioRDM.

Groups can be useful, for example, to externally manage access and roles of communities' members,
without hard coding the list of users in your InvenioRDM instance.
Another possible scenario, not yet supported, could be to grant or restrict access to other resources,
such as records or files.

The support of groups is a feature  introduced in the release
[v9.0](https://inveniordm.docs.cern.ch/releases/versions/version-v9.0.0/).

When integrating groups in your InvenioRDM instance, you will have to:

1. Import and keep in sync a copy of the groups available in your organization in the InvenioRDM database.
This is needed to be able to search for groups when granting/restricting access to resources.
2. When the user signs in, "assign" to the user the list of groups to which (s)he belongs. Read more below.

!!! notice
    How to import and keep in sync the local copy of groups with your organization' groups is outside the scope
    of the InvenioRDM documentation and highly depends on your organization's policies, constraints and technologies.

#### Add groups

In InvenioRDM, groups are simply treated as `Roles`. To add a group, you create a role:

```python
from invenio_accounts.proxies import current_datastore

current_datastore.create_role(name="it-dep", description="The group containing all users of the IT department.")
current_datastore.commit()
```

#### Assign groups on login

When the user signs in, you will have to add the user's groups as `needs` (technically `RoleNeed`).
If an intersection between the `RoleNeed` (the groups) that the user provides and the `RoleNeed` that the resource
requires exists, then the user has access.

With the example above, a user providing a `RoleNeed('it-dep')` will have access to a resource requiring the `RoleNeed('it-dep')`.

Below, you can find **an example** of how you can add a `RoleNeed` on login.

!!! warning "Use at your own risk"
    The integration of groups is not fully tested yet and the code below is just an example of a possible implementation.

Assuming you're implementing a custom
[OAuth plugin](https://inveniordm.docs.cern.ch/customize/authentication/#new-oauth-plugins),
the fetching of user groups can happen after having fetched user information with the
[`signup_handler.info`](https://inveniordm.docs.cern.ch/customize/authentication/#allowdeny-user-login) handler.

```python
def info_handler(remote, resp):
    ...
    # existing code
    user_info = get_user_info(remote, resp)
    ...
    # your implementation: fetch groups synchronously
    roles_or_groups_names = fetch_roles_or_groups_names(remote, user_info)
    provides = set(UserNeed(current_user.email))
    # add groups as Invenio roles to user session
    for name in roles_or_groups_names:
        provides.add(RoleNeed(name))
    identity.provides |= provides
    session["<my_external_app_name>_roles"] = provides
    # end your implementation
    ...
```

The `fetch_roles_or_groups_names` might retrieve the user groups from the `user_info` attributes previously fetched
or perform a new network request to fetch them from other REST APIs.

When groups cannot be retrieved synchronously in the same HTTP request (slow or heavy task), a possible solution could
be:

1. Fetch user groups async in a celery task and store it in the database. The `RemoteAccount` database table
   contains a `extra_data` column which could be used to "cache" user groups.
2. On login, enrich the user session identity `provides` by reading the list of groups from the database.
3. Refresh the list of user groups of each user when it makes sense in the organization context.
