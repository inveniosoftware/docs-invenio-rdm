# InvenioRDM v7.0

*2021-12-06*

## Try it

If you want to install the latest release, follow the installation instructions on [https://inveniordm.docs.cern.ch/install/](https://inveniordm.docs.cern.ch/install/) and choose version `v7.0`.

Want to see how it looks without installing it? Just head over to our demo site: [https://inveniordm.web.cern.ch](https://inveniordm.web.cern.ch).

## What's new?

### Basic OAI-PMH server

InvenioRDM v7.0 comes with a basic [OAI-PMH](https://www.openarchives.org/OAI/openarchivesprotocol.html) server. OAI-PMH is a standard for metadata harvesting among repositories and has a large adoption among different repository systems.

The OAI-PMH server in InvenioRDM supports most of the OAI-PMH standard except for sets. Sets support is being implemented and will be released in the coming InvenioRDM version.

**Try it**

You can access the server on (replace ``127.0.0.1`` with your host name):

- https://127.0.0.1/oai2d?verb=Identify
- https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc

**Restricted records**

The OAI-PMH standard doesn't say anything about authentication of requests. The OAI-PMH server in InvenioRDM however, supports both unauthenticated and authenticated requests using one of InvenioRDM's existing authentication mechanisms (browser sessions or access tokens). This means we're able to serve restricted records via the OAI-PMH server if the request is authenticated.


### DOI registration and persistent identifiers

We have made some large improvements to the stability and performance of the DOI registration. The overall user interface did not change, however the underlying backend changed.

**Asynchronous registration**

DOIs are now registered asynchronously so that the publishing is not delayed or blocked by e.g. DataCite being available or not.

**Metadata updates**

The DOI metadata is now updated in DataCite when a record is updated.

**URLs for landing pages**

We are now registering a landing page URL in DataCite of the form ``/doi/10.1234/foo.bar``. This ensures that, if in the future your URL patterns change, you do not have to overload DataCite with thousands to millions of update requests just to change a URL.

**Duplicate detection**

Duplicate detection now works properly, so that users cannot deposit multiple records with the same DOI.

**Blocked prefixes**

If the user provides an existing DOI, it's now possible to block specific DOI prefixes such as e.g. your local DataCite DOI prefix or e.g. the old DataCite test prefix such as ``10.5072``.

**Configuration improvements**

We revamped how the configuration is done. In addition, it is now possible to inject your own persistent identifier providers in case you have more advanced needs than the builtin DataCite DOI provider.



### Minor changes

**Web accessibility (A11y) fixes**

We have fixed a number of smaller web accessibility issues such as missing aria labels, color contrasts and the like. The work is continuing and more fixes are expected in the following InvenioRDM release.

**Increased default rate limits**

We have increased the default rate limits applied to guests and authenticated users, as it was quite easy to hit existing rate limits while browsing the site.

**Deletion of login IPs after 30 days**

We have added a new background task that runs on a daily basis. The task removes IP addresses which are tracked when a user logs in. By default IP addresses are kept for 30 days after which they are removed.

You can change the retention period using the configuration variable:

```python
ACCOUNTS_RETENTION_PERIOD = timedelta(days=30)
```

**CSRF improvements**

We have made a number of improvements to the Cross Site Request Forgery (CSRF) protection. CSRF happens when an attacker tricks a user into e.g. clicking a malicious link, which can then e.g. change email address and update password. The CSRF protection prevents these kinds of attacks.

The CSRF token was being regenerated on every HTTP request, however this could cause troubles with parallel REST API requests which would sometimes fail.

In addition, once a CSRF token expired, usually the user would be presented with an error. We have therefore implemented a transparent rotation of the tokens during a grace period, so that they are updated without the user hitting the CSRF errors.

**Accounts creation from CLI fixed**

A new release of Flask-WTF caused the Invenio command to not be able to create users. The change in Flask-WTF was properly deprecated but hadn't been fixed in InvenioRDM.

**Code: Unit of work pattern**

The backend has the concept of a service which provides a high-level interface into the business logic of the application. These services often provide methods that directly translate into e.g. a button being pressed on the user interface. Thus, these changes were mostly running in a single database transaction to ensure consistency.

However, we more and more often needed to group multiple service method calls into a single atomic database transaction. One of the issues with this was that indexing operations and background jobs should only be executed _after_ the database transaction was committed.

We therefore added a new [Unit of Work pattern](https://martinfowler.com/eaaCatalog/unitOfWork.html) that coordinates the database transaction commit with indexing and other background operations.

You'll see the new pattern used like the example below, and it only requires very few changes to your existing services:

```python
from invenio_records_resources.services.uow import \
    RecordCommitOp, unit_of_work,

@unit_of_work()
def create(self, ... , uow=None):
    # ...
    uow.register(RecordCommitOp(record, indexer=self.indexer))
    # Do not use `db.session.commit()` in service.

```



### Known issues

**Stale Data Error**

If you interact with the REST API or programmatically with the services using a script, you might hit this error. If you upload files and publish the associated drafts very quickly one after the other, you can risk that the publish sometimes fails. This is due to a concurrency issue, where background files processing extracts the width and height of an image and doesn't manage to finish before the publish is triggered.

The error happens because of the built-in concurrency protection in InvenioRDM that detects the issue (optimistic concurrency control). Therefore the bug does not cause any data integrity issues.

The work around is simply to read the record again, and publish it. Alternatively, your script can create all drafts first with associated files, and afterwards publish all the drafts.

See [https://github.com/inveniosoftware/invenio-rdm-records/issues/809](https://github.com/inveniosoftware/invenio-rdm-records/issues/809).

## Feature Preview

InvenioRDM v7.0 ships with a backend feature preview of the integration of records with communities and the new requests backend.

This is an important milestones which allows us to start the work on the frontend for the coming release in February.

All of the changes are backend-only, so you won't see any of the changes in the UI.

### Reviews

Records now support the concept of having reviews. We currently only ship one type of review which is for submitting a record to a community. An uploader will submit their draft to a community which can then accept/decline the draft through the review. When the submission is accepted, the draft is published and included in the community. If the submission is declined, the draft is not published nor included in the community.

The backend supports having multiple types of reviews, thus in the future you will be able to use the review feature for global curation workflows, spam checking and similar tasks.

### Requests

We have shipped a new module [Invenio-Requests](https://github.com/inveniosoftware/invenio-requests). The module basically implements an interface similar to GitHub pull requests. An entity (e.g. user) in the system can submit a request to a receiver (e.g. a community, another user, the system). The request is tied with automated actions upon accepting/declining/cancelling the request. Further, the creator and receiver of the request can communicate via comments and events can be logged on a timeline.

The module is a central piece for automating all sorts of user interactions such as e.g. file replacement, record deletion, user deletion, file quota increases, ownership transfers and the like.

### Full REST API flow

We have finished the overall REST API flow needed by the frontend which includes:

- An uploader selecting a community for a draft.
- An uploader submitting the request for inclusion to a community.
- The uploader cancelling their request.
- The curator accepting/declining the request.
- Any curator being able to see the draft (even restricted ones).
- The uploader/curator(s) commenting on the request.
- The uploader/curator(s) seeing the timeline of events related to a requests.
- The searching of requests both from a community's and from a user's dashboard.


## Upgrading to v7.0

We support upgrading from v6.0 to v7.0. Please see the [upgrade notice](../upgrading/upgrade-v7.0.md).

## Maintenance policy

InvenioRDM v7.0 is a **short-term support** (STS) release which is supported until InvenioRDM v8.0 (release currently planned for February 2022). See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v6.0 Long-Term Support (LTS) Release.

## Credit

The development work in this release was done by:

- Caltech (Tom)
- CERN (Javier, Jenny, Lars, Pablo, Zach)
- Northwestern University (Guillaume)
- NYU (Laura)
- TU Graz (David, Mojib)
- TU Wien (Max)
