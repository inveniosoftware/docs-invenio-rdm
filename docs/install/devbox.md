# Installation using Devbox

An alternative to the manual local install or the containerized installation is installing InvenioRDM locally with the tool [Devbox](https://www.jetify.com/devbox/). 

It provides a standardized way of installation that can be shared with other developers while still allowing easy access to and modification of local files.

More information on Devbox and InvenioRDM can be found in [this presentation](https://zenodo.org/records/12554567) from the Open Repositories 2024 conference.

Devbox uses the Nix package manager to provide the user with encapsulated shell sessions that handle their own system package dependencies (so you can have for example a Python and a node version living only in a devbox environment, not polluting your system outside of it).

!!! info "Information"

    The main difference between this method and the manual installation method is that you let `nix` manage the dependencies for you - no need to use `pyenv` or `nvm` to manage Python or Node versions for example. The provided installation script is just a small extra to make the installation even easier but it is not obligatory to use.

## Preparation

- On your machine you will need to install **Docker** and **Devbox** (as well as `git`):
    - Please read the [system requirements for Docker](https://inveniordm.docs.cern.ch/install/requirements/#docker) of InvenioRDM!
    - You can find the current Devbox installation guide [here](https://www.jetify.com/devbox/docs/installing_devbox/).
- Clone the [invenio-devbox repository](https://github.com/ulbmuenster/invenio-devbox) to your lcoal machine. It contains a pre-configured installation script that can later be adapted to match your instance's needs. This includes the installation of the Invenio CLI tool and the scaffolding of the project.

## Devbox installation

- Navigate to the invenio-devbox directory that you just cloned:
    - e.g. 
    ```
    cd $HOME/invenio_devbox
    ```
- Start the Devbox shell:
    ```
    devbox shell
    ```
- Install a fresh InvenioRDM instance with the [provided installation script](https://github.com/ulbmuenster/invenio-devbox/blob/main/devbox_scripts/install-empty.sh) which is using `invenio-cli` to set up the instance:
    ```
    devbox run install-empty
    ```
    - You will be prompted to enter a name for your new instance or accept the default *my-site*
    - Choosing a custom name that contains a dash (e.g. `test-instance`) leads to an error and should therefore be avoided.
- Navigate to your instance directory, e.g.:
    ```
    cd my-site
    ```
- Start your new InvenioRDM instance:
    ```
    invenio-cli run
    ```
- Open your browser and navigate to `https://127.0.0.1:5000`
    - Click the button for “Advanced…” options and click “Accept the risk and continue”
    - See the [notes in the Quick Start guide](https://inveniordm.docs.cern.ch/install/#5-explore-inveniordm) on why this is necessary.
- You can log in with the already activated admin account:
    - user: `admin@inveniosoftware.org` with password: `123456`
- Enjoy your fresh InvenioRDM installation!

The Devbox installation will behave like a local installation, so you can edit files easily and customize the instance to meet your requirements. You do not need to create or activate an admin account - this was already done by the installation script. Any other manual steps that apply to your installation can be added to this script as well, so you don't have to configure anything else after running it.
