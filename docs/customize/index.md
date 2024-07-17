# Customize InvenioRDM

**Intended audience**

This guide is intended for system administrators and developers that need to customize their
InvenioRDM instance, so that it integrates into their organizational environment.

## Customization hierarchy

To help you understand customization and use the appropriate methods, keep in mind the following hierarchy of customization. This hierarchy lists the customization approaches from "least involved, most well-supported, and least flexible" to "most involved, least supported, and most flexible" -from the shallow-end of the pool to the deep-end.

1. Set configuration values -- _least effort, most limited_.
2. Create and place files in expected locations.
3. Install modules (and set their configuration values).
4. Create your own modules and install them.
5. Make contributions to core modules.
6. Strike out on your own and fork modules (you do you!) -- _most effort, least limited_.

We recommend you exhaust the capacities of an approach before you reach out for a more involved one (e.g., don't create an extension to change the logo).

In the following sections, we cover customization opportunities that InvenioRDM provides. These span the gamut of level 1 to 4.

## Overview

- [Look-and-feel](look-and-feel/index.md) - change the appearance of InvenioRDM to match your institution.
- [DOI registration](dois.md) - mint DOIs with your institution's prefix.
- [Authentication](authentication.md) - integrate with your institutional authentication system.
- [Sending emails](emails.md) - integrate with your institutional email system.
- [Record landing page sections](record_landing_page.md) - customize sections of the record landing page.
- [S3 Storage](s3.md) - configure s3 as storage.
- [Upload Limits](upload_limits.md) - Set limits on file uploads for records.
- [Vocabularies](vocabularies/index.md) - use custom controlled vocabularies, default users and other institution specific data.
    - [Affiliations](vocabularies/affiliations.md)
    - [Names](vocabularies/names.md)
    - [Subjects](vocabularies/subjects.md)
    - [Users](vocabularies/users.md)
- [Internationalisation (i18n) and Localisation (l10n)](i18n-and-l10n.md)
- [Notifications](notifications.md) - customize content, recipients and backends of notifications
