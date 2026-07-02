# Archive code as records

_Introduced in v14_

![The GitLab menu on the user's account settings page, showing a list of projects](./imgs/vcs.png)

Using the optional [Invenio VCS](https://github.com/inveniosoftware/invenio-vcs) module, you can allow users to connect their accounts
from various Version Control System (VCS) providers and sync their repositories.
Each new release is published as a record in InvenioRDM with automatically imported metadata.

## Install the module

Invenio VCS is an optional module and is not included by default.
To start using it, you need to install it.

1. Add the dependency to your `pyproject.toml` file via `uv` or your chosen package manager.

    ```bash
    uv add invenio-vcs
    ```

2. Run a full install of the dependencies:

    ```bash
    invenio-cli install
    ```

3. Run the new database migrations:

    ```bash
    invenio alembic upgrade head
    ```

## Configure

Invenio VCS allows you to flexibly configure multiple VCS providers and allow users to sync their repositories.

Currently, the following VCS providers are officially supported:

- GitHub (including Enterprise)
- GitLab (including self-hosted)

However, you can add support for any other provider (including non-Git ones) by implementing an abstract class.

To set up the module:

1. Follow the [quick start steps](https://github.com/inveniosoftware/invenio-vcs/blob/master/docs/usage.rst#quick-start) in the Invenio VCS documentation.

2. Register the notification builders to ensure users can be notified about repository release events

    ```python
    # invenio.cfg

    from invenio_rdm_records.notifications.vcs import (
        RepositoryReleaseCommunityRequiredNotificationBuilder,
        RepositoryReleaseCommunitySubmittedNotificationBuilder,
        RepositoryReleaseFailureNotificationBuilder,
        RepositoryReleaseSuccessNotificationBuilder
    )
    from invenio_app_rdm.config import NOTIFICATIONS_BUILDERS

    NOTIFICATIONS_BUILDERS = {
        **NOTIFICATIONS_BUILDERS,
        RepositoryReleaseSuccessNotificationBuilder.type: RepositoryReleaseSuccessNotificationBuilder,
        RepositoryReleaseFailureNotificationBuilder.type: RepositoryReleaseFailureNotificationBuilder,
        RepositoryReleaseCommunityRequiredNotificationBuilder.type: RepositoryReleaseCommunityRequiredNotificationBuilder,
        RepositoryReleaseCommunitySubmittedNotificationBuilder.type: RepositoryReleaseCommunitySubmittedNotificationBuilder,
    }
    ```

3. Set Invenio VCS to use the InvenioRDM release class, which translates repository releases to records.

    ```python
    # invenio.cfg

    from invenio_rdm_records.services.vcs.release import RDMVCSRelease

    VCS_RELEASE_CLASS = RDMVCSRelease
    ```

4. Add the VCS component, which syncs changes to records' statuses with the VCS module.

    ```python
    # invenio.cfg

    from invenio_rdm_records.services.components.vcs import VCSComponent
    from invenio_rdm_records.services.components import DefaultRecordsComponent

    RDM_RECORDS_SERVICE_COMPONENTS = [
        **DefaultRecordsComponent,
        VCSComponent
    ]
    ```

That's it! Your configured provider(s) will be ready to use.

## Mandatory community usage

On instances where [a community is required to publish a record](./require_community.md), users will need to select
the target community for their releases when enabling a repository. 
They will be prompted to do so via a modal that appears when clicking the toggle switch.

![Community selection modal when enabling a repository](./imgs/vcs_require_community.png)

They will not be able to enable the repository without selecting a community.
For repositories enabled before the `RDM_COMMUNUITY_REQUIRED_TO_PUBLISH` was set to `True`, new releases will result in an error.
The user will be notified via an email and will be able to select a community, after which the record will be published.

## Upgrading from Invenio GitHub

As of [InvenioRDM v14](../../releases/v14/version-v14.0.md), [Invenio GitHub](https://github.com/inveniosoftware/invenio-github) is deprecated.
You can continue to use it for now, but support will be fully dropped in InvenioRDM v15.

If your instance was actively using Invenio GitHub (with at least one user having connected their GitHub account) **and**
you want to keep the existing data, you will need to follow [these steps](https://github.com/inveniosoftware/invenio-vcs/blob/master/docs/upgrading.rst)
to migrate to Invenio VCS.

If you were not using Invenio GitHub or you don't mind the data not being migrated, you do not have to follow these steps.

## Further customization

The behaviour of the VCS module can be customized via config variables as well as by overriding code.
Refer to the [module's documentation](https://github.com/inveniosoftware/invenio-vcs/tree/master/docs) for more details.
