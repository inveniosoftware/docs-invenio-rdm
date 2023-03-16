# Migrate Docker images

Docker terminated the Free Team organizations subscription on April 14, 2023. This means that the `inveniosoftware` on Docker Hub, a Free Team organization, will no longer exist.

## Impact on InvenioRDM

The base Docker images for InvenioRDM v9.x and v10.x were hosted on Docker Hub, under the `inveniosoftware` organization. When Docker will remove the organization, such images might not be available anymore. In a [second announcement](https://www.docker.com/blog/we-apologize-we-did-a-terrible-job-announcing-the-end-of-docker-free-teams/), Docker clarified that:

> ...public images will only be removed from Docker Hub if their maintainer decides to delete them.

Depending on what will happen, building the Docker images on InvenioRDM v9/v10 with the commands `invenio-cli containers ` might fail.

With InvenioRDM v11, released on January 26, 2023, we have migrated the Docker images to the CERN registry, see [here the release notes](../versions/version-v11.0.0.md#deployment). This was done for a couple of reasons:

1. Avoid [Docker Hub rate limits](https://www.docker.com/increase-rate-limits/).
2. Take advantage of the automatic security scan provided by the CERN registry.

With this new Docker announcement, it is hard to trust them in keeping such images available and free to use. Hosting images on CERN registry is now necessary.

## Migration

### Am I impacted?

If you are running InvenioRDM v9 or v10, you might be impacted at some point.

Independently of the InvenioRDM version that you are running, you can check if you are impacted by opening the `Dockerfile` file in your instance and by checking the first command `FROM`.

⚠️ These lines might fail:

```
FROM inveniosoftware/centos7-python:3.7
```
```
FROM inveniosoftware/centos8-python:3.8
```
```
FROM inveniosoftware/centos7-python:3.9
```

✅ These lines will work:

```
FROM registry.cern.ch/inveniosoftware/centos7-python:3.7
```
```
FROM registry.cern.ch/inveniosoftware/centos8-python:3.8
```
```
FROM registry.cern.ch/inveniosoftware/centos7-python:3.9
```
```
FROM registry.cern.ch/inveniosoftware/almalinux:1
```

### Should I act now?

It is not necessary to act immediately, but you might want to consider this migration in a near future. While Docker clarified with a second announcement that public images will still be available, it is not clear for how long and if they will be limited at some point.

### Migration

There are two possible ways to migrate:

1. Upgrade your InvenioRDM to v11. If you are running InvenioRDM v9, make sure that you upgrade first to v10, and then to v11. Be aware that InvenioRDM v11 is **not** a LTS version.
2. Change the Dockerfile to use `registry.cern.ch/inveniosoftware/*` instead of `inveniosoftware/*`.

    ```diff
    - FROM inveniosoftware/centos7-python:3.9
    + FROM registry.cern.ch/inveniosoftware/centos7-python:3.9
    ```

    or, using the latest AlmaLinux image:

    ```diff
    - FROM inveniosoftware/centos7-python:3.9
    + FROM registry.cern.ch/inveniosoftware/almalinux:1
    ```

    In this last case of AlmaLinux, make sure that you are running Python 3.9, which is the Python version that comes with the `almalinux` image. You should follow the [v11 Python version change](./upgrade-v11.0.md#python-version-change) instructions to make sure that you are taking the necessary steps.

!!! warning "Test!"
    The change of the base Docker image can lead to unexpected issues. We recommend testing your instance extensively in a test environment, before deployment to production.

## About images registry

The CERN registry for the InvenioRDM images is available to everyone. However, it is not a service with a guaranteed uptime, as the Docker Hub registry.

You might want to explore the usage of proxy caches within your organization (for example, using the open source [Harbor](https://goharbor.io/) or [Nexus](https://www.sonatype.com/products/nexus-repository)): it will help you having the InvenioRDM images always available, to dramatically increase network speed (local network download vs internet download) and to eventually by-pass any organization's restriction in bandwidth or speed.
