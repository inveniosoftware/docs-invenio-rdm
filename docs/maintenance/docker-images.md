# RDM Docker images

The official RDM Docker image(s) are available in the [docker-invenio](https://github.com/inveniosoftware/docker-invenio) repo.

Currently, the official base image uses `AlmaLinux v9` and is pushed to the [CERN registry](https://registry.cern.ch/).

## Building

The AlmaLinux image is automatically built via GitHub Actions when a tag is pushed. When pushing a new tag,
make sure that you check the current version in `FROM registry.cern.ch/inveniosoftware/almalinux:...` in
the current RDM Docker image.

## CERN registry

Docker images are pushed to the CERN registry [inveniosoftware](https://registry.cern.ch/harbor/projects/1825/repositories) project. This is done to:

1. March 2023: Docker announced that Free Team organizations, such as `inveniosoftware`, will be removed.
2. Avoid [Docker Hub rate limits](https://www.docker.com/increase-rate-limits/).
3. Take advantage of the automatic security scan provided by Harbor.

The project is configured with tag retention policies, so that the disk space is not filled up too quickly (see below).

## Security scans

Security scans are automatic on the CERN Registry, using [Trivy](https://github.com/aquasecurity/trivy).
You can run the scan locally installing Trivy or use the web app: <https://trivy.dev>.

At the moment, the security scans from the CERN Registry are not sending reports or alerts.

Security scans for Docker images are also being configured (work not yet completed) using GitHub Actions:
it is easier to configure alerts, notifications or scan reports and also GitHub security issues can be automatically created.

## Retention

This section Work In Progress: the development of the Docker images building process is not yet completed.

See: <https://github.com/inveniosoftware/docker-invenio/issues/68>

To allow the CERN Registry to send notifications to Discord, we have a created a small web app to convert the payload and deployed on OpenShift:

- GitHub repo: <https://github.com/inveniosoftware/alertabot>
- OpenShift project: `invenio-alertabot.web.cern.ch`
- Sentry: `InvenioRDM` project

This project might be archived when the GitHub Action development is completed, as it will already cover the features provided by this webapp.
