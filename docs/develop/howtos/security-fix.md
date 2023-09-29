# Fix a vulnerability

This guide describes the process for fixing a vulnerability and is intended
for InvenioRDM maintainers.

**TL;DR - don't communicate or fix publicly a vulnerability**

## Step 1 - Inform architects

First, report the issue directly to Invenio architects if they have not already
been alerted. If in doubt, report to
[info@inveniosoftware.org](mailto:info@inveniosoftware.org).

The architects are there to help facilitate the process.

## Step 2 - Inform reporter

An architect will acknowledge to a reporter that we have received the report,
and inform them about the process and our security policy.

## Step 3 - Create a draft advisory

Start a draft security advisory on the affected GitHub repository. For instance:

- [https://github.com/inveniosoftware/invenio-rdm-records/security/advisories/new](https://github.com/inveniosoftware/invenio-rdm-records/security/advisories/new)

Clearly describe the impact (use GitHub's default template), and fill in
all fields as well as affected packages.

## Step 4 - CVE score

Use the
[CVE scoring calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator)
to determine the CVE score and select

## Step 5 - Identify supported versions

Next, identify all supported versions of the module using the
[branch management](../../maintenance/branch-management.md) and take note of which branch(es)
you have to apply the fix to.

## Step 6 - Create a private temporary fork

The GitHub security advisory form allows you to create a temporary private
fork. Follow the instructions provided in the GitHub interface in order to
create it.

## Step 7 - Create branches and fix the issue

For each of the supported versions, make a branch in the private fork that
forks off from the correct master/maintenance branch.

If possible fix first on ``master/main``, then cherry-pick to the other
maintenance branches.

Also, remember to include release commits.

## Step 8 - Open pull requests against the private fork

Push your branches to the temporary private fork, and open pull requests
against the fork (the GitHub interface explains how).

## Step 9 - Request a CVE

## Step 10 - Send advance notification (2-5 days in advance)

Send out an advance notification that a security fix is being published in 2-5
days. Vulnerabilities should normally be released early in the week to provide
time for user to upgrade.

## Step 11 - Merge, release and publish
