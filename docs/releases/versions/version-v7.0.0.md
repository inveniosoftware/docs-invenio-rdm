# InvenioRDM v7.0

*2021-12-06*

## Try it

If you want to install it, follow the installation instructions on [https://inveniordm.docs.cern.ch/install/](https://inveniordm.docs.cern.ch/install/)

Want to try InvenioRDM? Just head over to our demo site: [https://inveniordm.web.cern.ch](https://inveniordm.web.cern.ch)

## What's new?

### Basic OAI-PMH server

InvenioRDM v7.0 comes with a basic [OAI-PMH](https://www.openarchives.org/OAI/openarchivesprotocol.html) server. OAI-PMH is a standard for metadata harvesting among repositories and have a large adoption among different repository systems.

The OAI-PMH server in InvenioRDM supports most of the OAI-PMH standard except for sets. The sets support is being implemented and will be released in the coming release.

**Try it**

You can access the server on (replace ``127.0.0.1`` with your host name):

- https://127.0.0.1/oai2d?verb=Identify
- https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc

**Restricted records**

The OAI-PMH standard doesn't say anything about authentication of requests. The OAI-PMH server in InvenioRDM however supports both unauthenticated and authenticated requests using one of InvenioRDMs existing authentication mechanisms (browser sessions or access tokens). This means we're able to serve restricted records via the OAI-PMH server if the request is authenticated.


### DOI registration and persistent identifiers

We have some large improvements to the stability and performance of the DOI registration. The overall user interface did not change, however the underlying backend changed.

**Asynchronous registration**

DOIs are now registered asynchronously so that the publishing is not delayed or blocked by e.g. DataCite being available or not.

**Metadata updates**

The DOI metadata is now updated in DataCite when a record is updated.

**URLs for landing pages**

We are now registering a landing page URL in DataCite of the form ``/doi/10.1234/foo.bar``. This ensures that if in the future your URL patterns changes, you do not have to overload DataCite with thousands to millions of update requests just to change a URL.

**Duplicate detection**

The duplicate detection now works properly so that users cannot deposit multiple records with the same DOI.

**Blocked prefixes**

If the user provide an exsisting DOI, it's now possible to block specific DOI prefixes such as e.g. your local DataCite DOI prefix or e.g. the old DataCite test prefix such as ``10.5072``.

**Configuration improvements**

We revamped how the configuration is done. In addition it is now possible to inject your own persitent identifier providers in case you have more advanced needs than the builtin DataCite DOI provider.



### Minor changes

**Web accessibility (A11y) fixes**

We have fixed a number of smaller web accessibility issues such as missing aria labels, color contrasts and the like. The work is continuing and more fixes are expected the coming InvenioRDM release.

**Increased default rate limit**

We have increase the default rate limits applied to guests and authenticated users, as it was quite easy to hit existing rate limits while browsing the site.

**Deletion of login IPs after 30 days**

We have added a new background task that runs on a daily basis. The task removes IP addresses which are tracked when a user logins. By default IP addresses are kept for 30 days after which they are removed.

You can change the retention period using the configuration variable:

```python
ACCOUNTS_RETENTION_PERIOD = timedelta(days=30)
```

**CSRF improvements**

We have made a number of improvements to the Cross Site Request Forgery (CSRF) protection. CSRF happens when an attacker tricks a user into e.g. clicking a malicious link, which can then e.g. change email addresses, update password and the link. The CSRF protection prevents these kinds of attacks.

The CSRF token was being regenerated on every HTTP request, however this could cause troubles with parallel REST API request which would somestimes fail.

In addition, once an CSRF token expired, usually the user would be presented with an error. We have therefore implemented a transparent rotation of the CSRF tokens during a grace period, so that the CSRF tokens is updated without the user hitting the CSRF errors.

**Accounts creation from CLI fixed**

A new release of Flask-WTF caused the Invenio command to not be able to created users. The change in Flask-WTF was properly deprecated but hadn't been fixed in InvenioRDM.

**Code: Unit of work pattern**

The backend has the concept of a service which provides a high-level interface into the business logic of the application. These services often provides methods that directly translate into e.g. a button being pressed in the user interface. Thus, mostly these changes were running in a single database transaction to ensure consistency.

However, we more and more often needed to group multiple services method calls into a single atomic database transaction. One of the issues for this was that indexing operations and background jobs should only be executed after the database transaction was committed.

We therefore added a new [Unit of Work pattern](https://martinfowler.com/eaaCatalog/unitOfWork.html) that coordinates the database transaction commit with indexing and background jobs operation.

You'll see the new pattern used like the example below, and only requires very few changes to your existing services:

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

If you interact with the REST API using a script you might hit this error. If you upload records via the REST API and the calls are made very fast after one another, you can risk that the publish sometimes fails. This is due to a concurrency issue, where background files processing extracts image/width and height and doesn't manage to finish before the publish.

The error happens because of the built-in concurrency protection in InvenioRDM that detects the issue (optimistic concurrency control). Therefore the bug does not cause any data integrity issues.

The work around is simply to read the record again, and publish it. Alternatively, your script can implement creation of all drafts first, and afterwards a phase of publishing the drafts.

See https://github.com/inveniosoftware/invenio-rdm-records/issues/809

## Feature Preview

InvenioRDM v7.0 ships with a backend feature preview of the integration of records with communities and the new requests backend.

This is an important milestones which allows us to start the work of the frontend for the coming release in February.

All of the changes are backend-only, so you won't see any of the changes in the UI.

### Reviews

Records now support the concept of having reviews. We currently only ship one type of review which is for submitting a record to a community. An uploader will submit their draft to a community who can the accept/decline the review. Upon accepting the review, the draft is published and included in the community.

The backend supports having multiple types of reviews, thus in the future you use the review feature for global curation workflows, spam checking and similar.

### Requests

We have shipped a new module Invenio-Requests. The module basically implements an interface similar to GitHub pull requests. An entity (e.g. user) in the system can submit a request to a receiver (e.g. a community, another user, the system). The request is tied with automated actions upon accepting/declining/cancelling the request. Further, the creator and receiveer of the request can communicate via comments and events can be logged on a timeline.

The module is a central piece for automating all sorts of user interactions such as e.g. file replacement, record deletion, user deletion, file quota increases, ownership transfers and the like.

### Full REST API flow

We have finished the overall REST API flow needed but the frontend which includes:

- An uploader selecting a community for a draft.
- An uploader submitting the request for inclusion to a community.
- The uploader cancelling their request.
- The curator accepting/decling the request
- The curator is able to see the draft (even restricted ones).
- The uploader/curators can comment on the request.
- The searching of requests both from a community and from a user dashboard.


## Upgrading to v7.0

We support upgrading from v6.0 to v7.0. Please see the [upgrade notice](../upgrading/upgrade-v7.0.md)

## Maintenance policy

InvenioRDM v7.0 is a **short-term support** release which is supported until InvenioRDM v8.0 (release currently planned for February 2022). See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v6.0 Long-Term Support Release.

## Credit

The development work in this release was done by:

- Caltech (Tom)
- CERN (Javier, Jenny, Lars, Pablo, Zach)
- Northwestern University (Guillaume)
- NYU (Laura)
- TU Graz (David, Mojib)
- TU Wien (Max)
