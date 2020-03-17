# How can I deploy InvenioRDM?

You can deploy InvenioRDM in several ways. You can install it in your [local computer](../develop/index.md) to have more easily customizable environment, otherwise you can deploy a [containerized environment](../preview/index.md) that demonstrates the setup of all components runnning in docker containers. In this section it is explained how to deploy in a closer-to-production manner.

!!! warning "Do not deploy as-is in production"
    Please note that it is mentioned as "closer-to-production", this is because even if the designed architecture can scale and withstand the load of a production service (It has been tested to stand peaks of up to 180 requests/s), the security configurations might not be enough and you should review it. In addition, it can deploy the extra services (Elasticsearch and PostgreSQL) along with them, however this ones are not configured with redundancy and persistance.

## Helm Charts

[Helm](https://helm.sh) is the package manager for [Kubernetes](https://kubernetes.io/). This means, that by using Helm charts you can deploy InvenioRDM in any cloud provider that supports Kubernetes (e.g. OpenShift clusters, Google Cloud, Amazon Web Services, IBM Cloud).

**What is a Helm chart?**

A Helm chart is a definition of the architecture of the system, meaning how all components interconnect with each other (In a similar fashion that a `docker-compose` file).

In addition, Helm allows you to **install, version and upgrade and rollback** your InvenioRDM installation in an easy way. You can find more information about Helm [here](https://helm.sh/docs/intro/quickstart/).

### Charts description

The currents charts propose the following architecture:

- HAProxy as entry point. It provides load balancing and queuing of the requests.
- Nginx as reverse proxy. It serves as reverse proxy, to help HAproxy and uWSGI "talk" the same language (protocol).
- Web application nodes, running the uWSGI application.
- Redis and RabbitMQ come along in containers.
- Elasticsearch and PostgreSQL can be added to the deployment, however they are not configured in-depth and therefore not suited for more than demo purposes.

For more in-depth documentation see the [services description](services.md) and the configuration available [here](configuration.md).

## Pre-Requirements

- [Helm](https://helm.sh/docs/intro/install/) version 3.x
- Adding the [helm-invenio](https://github.com/inveniosoftware/helm-invenio) repository

``` console
$ helm repo add helm-invenio https://inveniosoftware.github.io/helm-invenio/
$ helm repo update
$ helm search invenio

NAME                   	CHART VERSION	APP VERSION	DESCRIPTION
helm-invenio/invenio	0.2.0        	1.16.0     	Open Source framework for large-scale digital repositories
helm-invenio/invenio	0.1.0        	1.16.0     	Open Source framework for large-scale digital repositories
```

You can also install by cloning from GitHub by cloning the repository:

```
$ git clone https://github.com/inveniosoftware/helm-invenio.git
$ cd helm-invenio/
```

Then you will need, to reference the `./invenio` folder rather than the chart name (`helm-invenio/invenio`).

## Supported Platforms

!!! warning "Only compatible with OpenShift"
    Pleas note that currently these Helm charts are only compatible with OpenShift.

- [OpenShift](openshift.md)
- [Kubernetes](kubernetes.md)
