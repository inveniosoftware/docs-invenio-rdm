# Setup Sending Emails

## Adding Credentials

You can add your credentials for sending emails in `invenio.cfg`. For example:

``` python
SECURITY_EMAIL_SENDER = "reasearchdata@my-university.com"
"""Email address used as sender of account registration emails."""
"""Domain name should match the domain used in web server."""

MAIL_SERVER = "exhub.my-university.com"

MAIL_SUPPRESS_SEND = False
"""Enable email sending by default.
Set this to False when sending actual emails.
"""
```
For more possible adjustments see the
[flask-mail-documentation](https://pythonhosted.org/Flask-Mail/#configuring-flask-mail).

If `MAIL_SUPPRESS_SEND` is set to `True` you can find the 'sent' emails in the
logs of the worker:

``` shell
docker logs my-site_worker_1 --follow
```
where `my-site_worker_1` needs to be set to the actual name of your
docker-`worker`-container.

``` shell
worker_1      | 2021-11-16T12:47:41.813264403Z [2021-11-16 12:47:41,812: INFO/MainProcess] Received task: invenio_accounts.tasks.send_security_email[67a66b59-bd57-40f3-88d5-a8a47664c054]
worker_1      | 2021-11-16T12:47:41.816356495Z Content-Type: text/plain; charset="utf-8"
worker_1      | 2021-11-16T12:47:41.816422677Z MIME-Version: 1.0
worker_1      | 2021-11-16T12:47:41.816435089Z Content-Transfer-Encoding: 7bit
worker_1      | 2021-11-16T12:47:41.816444006Z Subject: Welcome to Invenio App RDM!
worker_1      | 2021-11-16T12:47:41.816452833Z From: reasearchdata@my-university.com
worker_1      | 2021-11-16T12:47:41.816461501Z To: testy@my-university.com
worker_1      | 2021-11-16T12:47:41.816492455Z Date: Tue, 16 Nov 2021 12:47:41 +0000
worker_1      | 2021-11-16T12:47:41.816502651Z Message-ID: <163706686174.78.14192334637904439697@e32d87039a90>
worker_1      | 2021-11-16T12:47:41.816512277Z
worker_1      | 2021-11-16T12:47:41.816520657Z This is my wonderful email-template in plain text!
worker_1      | 2021-11-16T12:47:41.816529772Z -------------------------------------------------------------------------------
```

## Templates

To override the standard welcome-email, add the following folders and files in
your `templates/` folder: `security/email/welcome.txt` and
`security/email/welcome.html`.

``` shell
templates
└── security
    └── email
        ├── welcome.html
        └── welcome.txt
```

Example text for `welcome.txt`:

``` jinja
This is my wonderful email-template in plain text!
```

Example text for `welcome.html`:

``` jinja
<h1>This is my wonderful email-template in html</h1>
```

You can change the subject of your email with:

``` python
SECURITY_EMAIL_SUBJECT_REGISTER = "Welcome to My University Repository!"
"""Email subject for account registration emails."""
```

If you do not want to send html you can disable it in `invenio.cfg` with:

``` python
SECURITY_EMAIL_HTML = False
"""Render email content as HTML."""
```

For further inspiration including translation and variables you can take a look
at the templates created in
[invenio-accounts](https://github.com/inveniosoftware/invenio-accounts/tree/master/invenio_accounts/templates/security/email).
