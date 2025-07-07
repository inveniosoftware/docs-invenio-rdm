# Curation checks

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide provides a high-level architectural overview of checks in InvenioRDM.

## Overview

Checks provide a way to run automated verification on draft review requests and record inclusion requests for a given community. As such, checks require both:

* A **community** that has at least one check configuration (config) defined
* A draft review or record inclusion **request**

Checks, as designed, cannot be run on a draft without both a community and a request.

## Check Config

A check config defines the parameters for a check in a community. Note that each [type of check](#check-component) requires a separate config so there can be multiple per community. See the [Operate an Instance](../../operate/customize/curation-checks.md) documentation for usage details.

## Check Run

A check run is the result of running the check rules against a draft or a record.

## Check Component

A check component is the code which executes the check on the record in accordance with the `params` defined in the database. At current there are two check components defined: 

* MetadataCheck — uses the [metadata check config schema](../../reference/checks_config.md) to verify the metadata of a record
* FileFormatsCheck - verifies the extensions of the records files to check if they adhere to an open standard.

Check components are designed so that future checks can interact with third-party systems.
