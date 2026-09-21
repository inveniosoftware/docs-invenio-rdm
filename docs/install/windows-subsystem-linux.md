# Installing InvenioRDM on Windows WSL

!!! warning "Experimental"

    These steps cover a local development installation of InvenioRDM inside Windows Subsystem for Linux 2 (WSL2). Installing directly on Windows is otherwise not supported. The installation has been validated with a Debian WSL2 distribution, but there has not been long-term usage of it yet. After we've had more time with it, we will remove the "Experimental" flag. Other WSL2 distributions than Debian have not been validated. 

## Preparing a WSL distribution

Before installing InvenioRDM, prepare a WSL distribution:

- Make sure [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/about#what-is-wsl-2) is installed on your Windows system.
- Install a **Debian** distribution according to the [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/install).
- The initial distribution setup is minimal, so update the installed packages:

  ```bash
  sudo apt update && sudo apt upgrade
  ```

## Install required packages

In addition to the packages mentioned in the [system requirements](../install/requirements.md), you may need to install the following packages, depending on your WSL distribution:

- [curl](https://curl.se/)
- [uv](https://docs.astral.sh/uv/)
- [gcc](https://gcc.gnu.org/)
- [pnpm](https://pnpm.io/)

You may also verify that the required packages listed in the [Dockerfile](https://github.com/inveniosoftware/docker-invenio/blob/master/debian/Dockerfile) are installed in your WSL distribution.

## A note on Docker

When using WSL, we recommend installing Docker Desktop on your Windows system. After setting up the WSL distribution, open Docker Desktop and enable [WSL integration](https://docs.docker.com/desktop/features/wsl/) for the desired distribution. Then restart the WSL distribution.

## Install InvenioRDM

You are now ready to follow the [installation steps](../install/index.md#quick-start) to install InvenioRDM.