# RDM Docker Images

The official RDM Docker image(s) are available in the [docker-invenio](https://github.com/inveniosoftware/docker-invenio) repo.

Currently, the official base image uses `AlmaLinux` `v9` and it is pushed to the CERN registry.

## Building

The AlmaLinux image is automatically built via GitHub Actions when a tag is pushed. When pushing a new tag,
make sure that you check the current version in `FROM registry.cern.ch/inveniosoftware/almalinux:...` in
the current RDM Docker image.

## CERN registry

## Security scans

You can test locally with: https://trivy.dev

## Retention

latest -> almalinux-00120
1.0.0 -> almalinux-00120

almalinux-00120
almalinux-12345

Decided: images are tagged with a digest, latest and version tags are updated to point to latest built image.
Use a GitHub CI action to make sure the Actions are not disabled after 60 days and that we can always rebuilt the images

New repo: `alertabot`
configuration charts in the repo
OpenShift new project: invenio-alertabot.web.cern.ch
Sentry: on InvenioRDM
UpTimeRobot: ???
