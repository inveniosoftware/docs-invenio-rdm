# How can I deploy InvenioRDM?

In previous sections, you could see how to install InvenioRDM in your [local computer](../develop/index.md) for development, and how to run [containerized environment](../preview/index.md) that demonstrates the setup of all components running in docker containers. In this section we cover how to deploy InvenioRDM in a closer-to-production manner.

!!! warning "Do not deploy as-is in production"
    Please note the "closer-to-production" statement, this is because even if the designed architecture can scale and withstand the load of a production service (It has been tested to stand peaks of up to 180 requests/s), you need to review the security configurations and customize resources to fit your use case. In addition, Elasticsearch and PostgreSQL can be deployed along with the application, however they are not configured with redundancy and persistance in mind.

## Helm Charts

[Helm](https://helm.sh) is the package manager for [Kubernetes](https://kubernetes.io/). This means, that by using Helm charts (packages in Helm lingo) you can deploy InvenioRDM in any cloud provider that supports Kubernetes (e.g. OpenShift clusters, Google Cloud, Amazon Web Services, IBM Cloud).

**What is a Helm chart?**

A Helm chart is a definition of the architecture of the system, meaning how all components interconnect with each other (Similar to a `docker-compose` file).

In addition, Helm allows you to **install, version, upgrade and rollback** your InvenioRDM installation in an easy way. You can find more information about Helm [here](https://helm.sh/docs/intro/quickstart/).

### Chart description

The current chart proposes the following architecture:

- HAProxy as entry point. It provides load balancing and queuing of requests.
- Nginx as reverse proxy. It serves as reverse proxy, to help HAproxy and uWSGI "talk" the same language (protocol).
- Web application nodes, running the uWSGI application.
- Redis and RabbitMQ come along in containers.
- Elasticsearch and PostgreSQL can be added to the deployment. However they are not configured in-depth and therefore not suited for more than demo purposes.

For more in-depth documentation see the [services description](services.md) and the configuration available [here](configuration.md).

## Pre-Requirements

- [Helm](https://helm.sh/docs/intro/install/) version 3.x
- Adding the [helm-invenio](https://github.com/inveniosoftware/helm-invenio) repository.

To install Helm, follow the official documentation linked above. Once you have it installed you can [add
the repository](https://helm.sh/docs/helm/helm_repo_add/). The syntax is as follows:

``` console
helm repo add [NAME] [URL] [flags]
```

Let's add the `helm-invenio` (NAME) repository and check that it has been added correctly:

``` console
$ helm repo add helm-invenio https://inveniosoftware.github.io/helm-invenio/
$ helm repo update
$ helm search invenio

NAME                   	CHART VERSION	APP VERSION	DESCRIPTION
helm-invenio/invenio	0.2.0        	1.16.0     	Open Source framework for large-scale digital repositories
helm-invenio/invenio	0.1.0        	1.16.0     	Open Source framework for large-scale digital repositories
```

You can also install by cloning from GitHub:

```
$ git clone https://github.com/inveniosoftware/helm-invenio.git
$ cd helm-invenio/
```

In this case, you will need to reference the `./invenio` folder rather than the chart name (`helm-invenio/invenio`).

## Supported Platforms

!!! warning "Only compatible with OpenShift"
    Please note that currently this Helm chart is only compatible with OpenShift.

- [OpenShift](openshift.md)
- [Kubernetes](kubernetes.md)
