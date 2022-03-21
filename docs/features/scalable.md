---
hide:
  - toc
template: features_sub.html
image: ../images/scalable.png
summary: InvenioRDM scales with you! Handle 1 or 100 million records, 1 byte or several petabytes. It runs on bare-metal, VMs and container platforms such as Kubernetes and OpenShift. InvenioRDM powers very large repositories such as Zenodo.
---

## Build on giants

InvenioRDM under the hood relies on strong open source software such as PostgreSQL and Elasticsearch/OpenSearch.

## Large file support

InvenioRDM supports uploading and handling TB-sized files and can manage from few MBs to PBs of data as long as your underlying storage cluster supports it.

## Any file format/size

InvenioRDM accepts any file format in any size given that your underlying storage infrastructure can support it.

## Versioning support

Records and files are all versioned and our versioning feature performs automatic deduplication: so when 10KB of files change in a 100TB dataset we only store the new 10KB.

## Multi-storage systems

InvenioRDM allows you to integrate multiple storage systems in the same instance such as S3, XRootD and more.

## Deploy anywhere

InvenioRDM is a Python application and you can deploy into your institutional infrastructure whether it is on bare metal, VMs, containers, Kubernetes or OpenShift.

## Battle-tested

InvenioRDM is going to power [Zenodo.org](https://zenodo.org) with more than 3 million records, 1 peta-byte of data and 15 million visitors/year.
