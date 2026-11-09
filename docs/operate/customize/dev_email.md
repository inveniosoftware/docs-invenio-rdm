# Capture e-mails in development

This guide is meant for users that are in **development** and need to test e-mails receival / sending.

## Step 1 - run a local SMTP server

First, install a tool that runs a local SMTP server for testing purposes. This tutorial will use [Mailpit](https://github.com/axllent/mailpit).

If a system is not listed below, check the original documentation on how to install `Mailpit`.

### MacOS

```terminal
brew update && brew install mailpit
```

and then start Mailpit via

```terminal
mailpit
```

### Docker version

```terminal
docker run --restart unless-stopped --name mailpit -p 1025:1025 -p 8025:8025 -d axllent/mailpit
```

Note that, by default, `Mailpit` uses the following ports:

- `SMTP` server runs in port `1025`
- `HTTP` server runs in port `8025`.

Validate that `Mailpit` is running by accessing its `HTTP` server in [`http://127.0.0.1:8025`](http://127.0.0.1:8025) (or the configured `HTTP` server port).

## Step 2 - enable e-mails for development

In development, e-mail sending is disabled by default and the application must be configured for e-mails to be sent.

### Enable e-mail sending

E-mail sending is configured using the config `MAIL_SUPPRESS_SEND`. It must be set to **False** for e-mails to be sent to the configured `SMTP` server.

If set to **True**, e-mails are printed in `stdout` instead of being sent to the configured mail server.

Configure the application by editing the app's `invenio.cfg`:

```terminal
code src/my-site/invenio.cfg
```

```python
# Allow e-mails to be sent
MAIL_SUPPRESS_SEND = False

# Configured SMTP server's host
MAIL_SERVER = '127.0.0.1'

# Configured SMTP server's port
MAIL_PORT = 1025
```

Restart the application and e-mails will be sent to the configured `SMTP` server.

Check the inbox in [Mailpit UI](http://127.0.0.1:8025).

## Further reading

- How to configure flask mail - [docs](https://flask-mail.readthedocs.io/en/latest/#configuring)
- Mailpit - [original repo](https://github.com/axllent/mailpit)
