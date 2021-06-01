# Authentication

InvenioRDM supports local authentication only, integration with your institutional authentication
system only (e.g. OAuth, SAML, Single Sign-on) or both at the same time.

## Local Authentication

By default, it is only the only authentication system enabled. Users can create a new account using the
registration form and activate their account after the email confirmation.

You can disable local authentication by setting in `invenio.cfg`:

```python
ACCOUNTS_LOCAL_LOGIN_ENABLED = False  # allow/deny users to login with a local account
```

In case that local login is disabled, **it is recommended** to disable the possibility to register
new local account and change/recover passwords:

```python
SECURITY_REGISTERABLE = False  # allow/deny new users to register locally
SECURITY_RECOVERABLE = False  # allow/deny resetting the local account's password
SECURITY_CHANGEABLE = False  # allow/deny changing passwords for local accounts
```

!!! warning "Make sure that your configuration is consistent!"
    While *some* clearly inconsistent configurations (e.g. having `SECURITY_REGISTERABLE=True`
    and at the same time `ACCOUNTS_LOCAL_LOGIN_ENABLED=False`) will trigger a console **warning**
    when running the Invenio webserver, other inconsistent combinations may be silently
    accepted and ultimately result in unexpected behaviors.

## External authentication

InvenioRDM supports external authentication out-of-the-box, such as OAuth. SAML authentication
can also be experimentally enabled.

### OAuth

In addition to local accounts, InvenioRDM offers the possibilty to integrate external
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
See the plugin [documentation](fhttps://invenio-oauthclient.readthedocs.io/en/latest/usage.html#module-invenio_oauthclient.contrib.orcid)
for more information.

#### Keycloak

[Keycloak](https://www.keycloak.org/) is an open-source solution for identity management
that can be used for single sign-on endpoints.

##### Configuration

Information required to configure the InvenioRDM instance:

* The base URL (including port) of the Keycloak server.
* Information about the client, as configured in Keycloak:
    * Its realm
    * The client ID
    * The client secret
    * The target audience of Keycloak's JWTs (probably the same as the client ID)


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
remote_app["params"]["app_key"] = "OAUTHCLIENT_ANOTHER_NAME_APP_CREDENTIALS"
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
with `False` will be taken from the user input in the registration from.

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

Additional security-related configuration items can be found in the
[documentation for Flask-Security](https://flask-security.readthedocs.io/en/latest/configuration.html).

You can change the default duration (31 days) of the logged in user session (the session cookie expiration).
This is particularly useful when configuring InvenioRDM with external authentication only and you want to
have the InvenioRDM session duration as the external authentication provider session duration.

In your `invenio.cfg`:

```python
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
```

## Advanced integrations

### Custom login page

You can customize the login page template to display different information or
change its look and feel.

Start from an existing template:

* if you have local login only, copy the folder [templates/semantic-ui](https://github.com/inveniosoftware/invenio-accounts/tree/master/invenio_accounts/templates/semantic-ui) from `invenio-accounts`.
* if you have external authentication, copy the folder [templates/semantic-ui](https://github.com/inveniosoftware/invenio-oauthclient/tree/master/invenio_oauthclient/templates/semantic-ui) from `invenio-oauthclient`.

Then, open the `templates` folder in `my-site` (your instance) and paste it there. Inside the
`invenio-accounts`/`invenio-oauthclient` folder, keep only the template file that you want to customize.

Edit the Jinja template as you need.

For more information, see the guide [style other pages](/customize/styling/#change-other-pages).

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

```python
from invenio_oauthclient.utils import create_registrationform
from invenio_userprofiles.forms import ProfileForm
from wtforms import BooleanField, validators, FormField
from werkzeug.local import LocalProxy
from flask import current_app, url_for

_security = LocalProxy(lambda: current_app.extensions['security'])

# create a link to a PDF file containing the terms and conditions
# the PDF file is located in the `static/documents` folder.
terms_of_use_url=url_for("static", filename=("documents/terms-of-use.pdf"))
terms_of_use_text = f"Accept the <a href='{terms_of_use_url}' target='_blank'>terms and conditions</a>"

def my_registration_form(*args, **kwargs):
    # optionally, have different registration forms depending on the authentication
    # provider used by the user to login
    current_remote_app = kwargs.get("oauth_remote_app")
    if not current_remote_app:
        # return default just in case something is wrong
        return create_registrationform(*args, **kwargs)
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

# use the custom form function
OAUTHCLIENT_SIGNUP_FORM = my_registration_form
```

### New OAuth plugins

If you need to implement your own OAuth plugin to enable integration with your OAuth provider,
you can take advantage of the available OAuth helper class. You will need anyway to implement some
authentication handlers depending on your server authentication workflow. You can take a look
to existing implementations in [Invenio-OAuthClient](https://invenio-oauthclient.readthedocs.org).

In your `invenio.cfg`:

```python
class MyOAuthSettingsHelper(OAuthSettingsHelper):
    def __init__():
        super().__init__(
            title="my plugin",
            description="a description",
            base_url="https://myserver.com/,
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
    myoauth=myOAuthHelper.REMOTE_APP,
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

* **Identity Provider (IDP)**: performs authentication and passes the user's identity and authorization level to the service provider.
* **Service Provider (SP)**: trusts the identity provider and authorizes the given user to access the requested resource.

#### Prerequisites

* Make sure you have installed in your system:

    `libxml2-dev libxmlsec1-dev`

* Make sure you have installed the required Invenio Python module:

    ```console
    cd my-site
    pipenv run pip install invenio-saml
    ```

#### Server information

List of information required to configure the InvenioRDM instance.

* SAML requires a x.509 cert to sign and encrypt elements like `NameID`, `Message`, `Assertion`, `Metadata`.

    * **sp.crt**: the public cert of the SP
    * **sp.key**: the private key of the SP

* **EntityID**: Identifier of the IdP entity  (must be a URI)
* **SSO(singleSignOnService)**: URL Target of the IdP where the Authentication Request Message will be sent.
* **SLO(singleLogoutService)**: URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)
* **x509cert**: Public X.509 certificate of the IdP
* **Attributes mapping**: IDP in Assertion of the SAML Response provides a dict with all the user data:

    For example, given the following SAML response:

    ```json
    {
        "cn": ["Jhon"],
        "sn": ["Doe"],
        "mail": ["john.doe@example.com"],
        "external_id": ["24546786764d"]
    }
    ```

    You can create a mapping to the user account fields required by Invenio as the following:

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

        'settings':{
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
    }
}
```

#### Show the login button

The last step is to enable the login template, provided by the SAML module, to display the new button
`Login with SAML`.
In your `invenio.cfg`:

```python
OAUTHCLIENT_LOGIN_USER_TEMPLATE = "invenio_saml/login_user.html"
```

#### Multiple SAML authentication providers

You might have the need to integrate multiple SAML authentication providers at the same time, to allow users to login with one or the other.
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
    },
    # Second authentication provider
    "remote_app2": {
                 ....
     'settings': {
                 ....
                   },
                 ....
       'acs_handler': acs_handler_factory('remote_app2'),
    },
}
```
