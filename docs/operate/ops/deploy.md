# Deploy to production

This guide explains how to deploy InvenioRDM in a production environment.

!!! info "Read the infrastructure architecture first!"

    This guide assumes you understand the services required to run InvenioRDM
    and how they interact. See [Infrastructure architecture](./infrastructure.md)
    for details.

## Size your infrastructure

The following are **baseline requirements** for a small InvenioRDM production deployment.
Adjust based on your expected traffic, data volume, and performance requirements.

**Lightweight services:**
- HAProxy: 0.1 CPU, 100 MB memory
- Nginx: 0.1 CPU, 100 MB memory
- Redis: 0.1 CPU, 250 MB memory
- RabbitMQ: 0.5 CPU, 1 GB memory

**Application nodes:**
- Web nodes: 0.1 CPU, 300-400 MB memory per Python process
- Worker nodes: 1+ CPU, 300-400 MB memory per Python process

**Data services:**
- PostgreSQL: 1 CPU, 1-2 GB memory
- OpenSearch (master/data nodes): 1-2 CPUs, 2-4 GB memory

**Storage:**
- A few GB are sufficient for PostgreSQL, OpenSearch, Redis, and RabbitMQ
- For InvenioRDM application files, estimate based on your expected upload volume

See each service's official documentation for detailed requirements.

!!! note
    These are reference values for a small setup. Scale resources based on your traffic, data volume, and performance expectations.

## Deployment strategies

Choose a deployment strategy based on your needs, experience, and available resources.
Adapt this reference guide to your specific requirements.

### Docker Compose

The simplest deployment method uses Docker Compose with a configuration similar to
[the reference file in your InvenioRDM project](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/master/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-compose.full.yml).

!!! warning
    The provided Docker Compose file is designed for development and reference.
    **You must customize it for production use.**

**Suitable for small instances:**
- Thousands of records
- Tens of concurrent users

A single server with 4 vCPUs and 16 GB memory is typically sufficient.

!!! warning
    Docker Compose is primarily a development tool.
    While it simplifies deployment and can get you to production quickly,
    be aware of its limitations for production environments.

**Key considerations:**
- Mount volumes for all services (database, search, cache, queue) to persist data across restarts
- For local file storage, use a **backed-up volume** to prevent data loss
- Customize configuration by injecting environment variables (see [Configure everything](../customize/configuration.md))
- A single-server deployment may become insufficient as records and users grow;
  scale up the server first, then consider horizontal scaling
- Review critical [network security aspects](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
  to avoid exposing your infrastructure to the internet

### Virtual Machines (Infrastructure as a Service - IaaS)

At CERN, Invenio v3 instances run on [OpenStack](https://www.openstack.org).
For InvenioRDM, you can either:
- Install all services on a single large VM, or
- Distribute services across multiple VMs (similar to Docker Compose distribution)

**Suitable from small to large instances, scalable.**

### Kubernetes/OpenShift (Platform as a Service - PaaS)

For containerized deployments, at CERN we use [OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift)
with the [Invenio Helm Charts](https://github.com/inveniosoftware/helm-invenio).
These charts also work with [Kubernetes](https://kubernetes.io) clusters.

**Suitable from small to large instances, scalable.**

## Checklist

### Services

Start by installing and configuring all **required services**. Follow official documentation for each.

**1. Database (PostgreSQL):**
- Install and configure securely
- Create an unprivileged user with database creation and management permissions
- This user should only have database deletion rights if you need to use InvenioRDM wipe scripts
- Ensure remote connectivity from application servers
- **Restrict external network access**
- Implement **backup and recovery** strategies

**2. Search engine (OpenSearch):**
- Install and configure securely
- Set up a master node and at least one data node
- Restrict access to a dedicated user
- Ensure remote connectivity from application servers
- **Restrict external network access**
- Implement **backup and recovery** strategies
- Note: View and download statistics are **only stored in OpenSearch** (not the database) - back these up
  See [Usage statistics](../../maintenance/internals/statistics.md)

**3. Cache (Redis):**
- Install and configure securely
- Ensure remote connectivity from application servers
- **Restrict external network access**

**4. Message queue (RabbitMQ):**
- Install and configure securely
- Enable **queue persistence** to prevent task loss on service failure
- Ensure remote connectivity from application servers
- **Restrict external network access**

### InvenioRDM application

Install all requirements, then install the InvenioRDM Python application.
See the official [InvenioRDM Docker images](../../maintenance/operations/docker-images.md) for what packages to install.

**Configure the application:**
1. Open the `invenio.cfg` file
2. Adjust configuration for production, including service connections
3. Test the web app and worker for errors:

```bash
$ invenio run --extra-files invenio.cfg
$ celery -A invenio_app.celery -l INFO
```

**Build assets:**

```bash
$ invenio assets build
```

**Start the application server:**

Review the uWSGI configuration and run the server.

**Start Celery schedulers:**

```bash
$ celery -A invenio_app.celery beat -l INFO
$ celery -A invenio_app.celery beat -l INFO --scheduler invenio_jobs.services.scheduler:RunScheduler
```

### Serve HTTP traffic

**Install and configure Nginx reverse proxy:**
- Serve static assets directly from the build directory
- Forward backend requests to the uWSGI server

**Configure SSL termination:**
- If using HAProxy as load balancer, configure HTTPS certificates and SSL termination on HAProxy
- Otherwise, configure SSL on Nginx

**Expose your services:**
- Expose only HAProxy or Nginx IPs
- Configure DNS to route traffic to your reverse proxy/load balancer

**Security:** Only the load balancer/reverse proxy should be internet-facing.
All other infrastructure components must be isolated from external network access.

## Pre-launch checklist

Before making your instance publicly available, verify everything works:

1. **Open the website on your configured domain**
   - Verify HTTPS is working properly with valid certificates
   - Confirm the homepage loads without errors

2. **Create an admin user**

   ```bash
   $ invenio users create admin@your-institution.org --password -a --active
   ```

   - Replace `admin@your-institution.org` with your admin email
   - The `-a` flag grants admin privileges
   - The `--active` flag activates the account immediately

3. **Login with the admin user**
   - Use the credentials you just created
   - Verify you can access the administration interface

4. **Try to upload a new draft**
   - Create a new draft record
   - Upload a test file
   - Verify the file uploads successfully
   - Confirm that the draft appears in your uploads

5. **Check the Jobs in the admin panel and run them**
   - Navigate to the admin panel's "Jobs" section
   - Verify background tasks are processing correctly
   - Run any pending jobs if needed

## Versioning

As your project evolves, you will add custom features or upgrade InvenioRDM versions.
Versioning helps control which code is deployed.

At CERN, we use GitHub tags/releases (e.g., `v1.0.0`) for version management.

**Containerized deployments:**
- Automate image builds using [GitHub Actions](https://github.com/features/actions) or other CI tools
- Some PaaS platforms can auto-detect new images for specific tags (e.g., `production`)
  and trigger automatic redeployment

## Monitoring

After deployment, comprehensive monitoring provides observability into your infrastructure.

**Log aggregation:**
- Configure services to output logs to a central location
- Aggregate logs for dashboard visualization using tools like:
  - [Loki](https://grafana.com/oss/loki/)
  - [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/index/)

**System monitoring (IaaS):**
- Aggregate system logs to monitor resource consumption
- Collect metrics with [Prometheus](https://prometheus.io)
- Visualize with [Grafana](https://grafana.com)

**Application-specific monitoring:**
- Monitor Celery workers with [Flower](https://flower.readthedocs.io/en/latest/)
- Many tools can integrate with Prometheus

For IaaS deployments, store logs on servers with log rotation regardless of your chosen monitoring tool.

### Alerting

Once monitoring is configured, set up alerts for code exceptions and when metrics
reach configured thresholds.

**For the InvenioRDM Python application:**
[Sentry](https://sentry.io/welcome/) provides detailed exception information
(variables, stack traces, etc.). **Highly recommended** for production error debugging.

**Grafana ecosystem:**
- Use [OnCall](https://grafana.com/products/oncall) for alert management
- Configure messaging apps with [Grafana webhooks](https://grafana.com/docs/grafana/latest/alerting/manage-notifications/webhook-notifier/)

## Security

**To secure your instance:**

- [Correctly configure](../customize/configuration.md) your InvenioRDM instance
- Use valid HTTPS certificates
- Keep your instance and all services up-to-date

**Secure file uploads:** Be extremely careful with user-uploaded content, as served files
could contain malicious code. Effective protection methods:
- Whitelist MIME types
- Sanitize MIME types to prevent browser execution (e.g., convert HTML to plain text)
- Serve files from a separate domain using a static server without sessions

!!! note
    This is not an exhaustive list. Refer to established security literature and
    best practices for infrastructure security.

## Load testing

Understand your system's load capacity to properly size infrastructure.
Test with tools like:
- [Locust](https://locust.io)
- [k6](https://k6.io)

## Troubleshooting

**First step:** Identify which layer or service has the problem using:
- Monitoring and dashboard tools (see above)
- Direct log file inspection

**For InvenioRDM Python application issues:**
- Get detailed error information from Sentry
- Reproduce and debug in a local installation

See [How to debug](../code/debugging.md) for more information.
