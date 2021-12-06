# Features

Following is a high-level overview of features currently supported by InvenioRDM.

### Records

- **Any resource type** InvenioRDM allows you to store publications, datasets,
  software, images, videos or any other resource type you may have thus can
  serve as a single repository for all your records.

- **Any file format/size** InvenioRDM accepts any file format in any size given
  that your underlying infrastructure can support it.

- **Versioning support** Records and files are all versioned with optimized
  storage for large files.

- **DOI registration via DataCite** InvenioRDM can register DOIs with DataCite
  for all records, and allows you to write plugins for other identifier schemes.

- **DataCite-based metadata** InvenioRDMs internal metadata is based on the
  DataCite Metadata Schema which is a simple yet powerful format for describing
  nearly any research output (paper, data, software, ...).

- **Strong support for persistent identifiers** Authors, affiliations, licenses,
  related papers/datasets etc can all be identified via persistent identifiers
  such as ORCID and RORs.

- **Extended Date Time Format (EDTF) support** Publication dates and other dates
   support the EDTF format for recording imprecise dates and date ranges such
   as ``1939/1945``.

- **Previewers** InvenioRDM comes with previewers for common files formats such
  as PDFs, images, CSV, Markdown, XML and JSON.

- **Citation formatting** InvenioRDM can generate citations strings for your
  records using the Citation Style Language with support for more than 800+
  journal citation styles.

- **Record preview** Before you publish your record, you can see a preview of
  how it looks like.

- **Metadata-only records** Both records with or without associated files are
  supported.

- **Identifier detection and validation** InvenioRDM comes with support for
  automatic detection and validation for a large number of persistent identifier
  schemes (i.e. less typing and clicking for end-users).

### Search

- **Faceted search** InvenioRDM supports fully customizable faceted search.

- **Advanced query syntax** InvenioRDM has support for advanced querying via
  simple term search, phrase search, range search, regular expressions and
  custom ranking/sorting.

- **Auto-complete as you type** InvenioRDM exposed advanced APIs for
  search-as-you-type scenarios.

### Auth, permissions and security

- **Login via institutional account** InvenioRDM makes it easy to integrate your
  institutional authentication provider such as e.g. Keycloak, OAuth or alternative
  use e.g. ORCID for login.

- **Restricted records** InvenioRDM supports restricting access to files only
  or to the entire record.

- **Share by link** Restricted records can be shared with peer-reviewers or
  your colleagues via secret links.

- **Embargo support** Restricted records can be embargoed so that they are
  automatically made publicly on a specific date so that you can comply with
  e.g. funders' Open Access mandates.

- **Logged in devices** InvenioRDM allows users to see a list of currently
  logged in devices on their account.

### Customizations

- **Styling and theming** InvenioRDM can be styled and themed to fit into your
  institutional visual identity.

- **Custom vocabularies** All vocabularies such as types for resources, dates,
  roles, relations, affiliations etc can be customized to your local instance.

- **Subjects** InvenioRDM can load external subjects vocabularies used for
  classifications such as Medial Subject Headings (MeSH) and many others.

- **Permission system** InvenioRDM supports advanced customizations to the
  permission system for e.g. IP-based access control.

- **Persistent identifiers** Use the built-in support for DOIs, or add your
  own persistent identifier providers for other schemes.

### APIs and interoperability

- **REST API** InvenioRDM exposes a strong versioned REST API for all operations
  on the repository, that allows you to build your own integrations on top of
  InvenioRDM.

- **Export formats** InvenioRDM supports exporting records metadata in multiple
  formats such as JSON, Citation Style Language JSON, DataCite JSON/XML, Dublin
  Core.

- **OAI-PMH server** InvenioRDM ships with a built OAI-PMH server to allow
  metadata harvesting of records in your repository.

### Infrastructure

- **Large file support** InvenioRDM supports uploading and handling TB-sized
  files and can manage from MBs to PBs of data as long as your underlying
  storage systems supports it.

- **Multi-storage systems** InvenioRDM allows you to integrate backend multiple
  storage systems in the same instance such as S3, XRootD and more.

- **Deploy anywhere** InvenioRDM is a Python application and you can deploy
  into your institutional infrastructure wheather it is on bare metal, VMs,
  containers, Kubernetes or OpenShift.
