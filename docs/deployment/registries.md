# Image registries

There are several places where you can store your docker image. In this section, we cover some of the most known ones.
However, you can use any other of your preference.

!!! warning "Build your image before hand"
    In the following documentation we are assuming that you have already built your docker image.
    You can find documentation on how to do it [here](./image.md).

## DockerHub

To use docker hub, follow Docker's [official documentation](https://docs.docker.com/docker-hub/repos/).

## GitHub

To store your image in GitHub you will need a repository. You can use your instance's one. For example:
*https://github/yourusername/rdmrepo*. In addition, you will need to [create an access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). This access token must have
`read:packages` and `write:packages` scopes.

The first step is to log in to GitHub's docker registry:

``` console
$ docker login docker.pkg.github.com -u <YOU_GITHUB_USERNAME> -p <YOUR_GITHUB_TOKEN>
```

Then, find your docker image and tag it with the url of your GitHub registry:

```
$ docker images
REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
demo-inveniordm                                     latest              9b6dd5ae6b48        17 hours ago        2.33GB

$ docker tag demo-inveniordm docker.pkg.github.com/yourusername/rdmrepo/rdmimage:latest
```

!!! info "Project name"
    Note that `rdmrepo` is the name of your GitHub repository. Therefore the tag is: ``docker.pkg.github.co/<your_github_user_name>/<your_github_repo_name>/<your_image_name>:<version>``

Check that it was tagged correctly:

``` console
$ docker images                                                                   
REPOSITORY                                                      TAG                 IMAGE ID            CREATED             SIZE
demo-inveniordm                                                 latest              9b6dd5ae6b48        17 hours ago        2.33GB
docker.pkg.github.com/yourusername/rdmrepo/rdmimage:latest      latest              9b6dd5ae6b48        17 hours ago        2.33GB
```

The last step is to push your package to the GitHub registry:

``` console
docker push docker.pkg.github.com/yourusername/rdmrepo/rdmimage:latest
```

In order to use this image, you must set the following value in your `values.yaml` file (for both `web` and `worker`):

```
web:
    image: docker.pkg.github.com/yourusername/rdmrepo/rdmimage:latest

worker:
    image: docker.pkg.github.com/yourusername/rdmrepo/rdmimage:latest
```

Even if your project and/or image is public, GitHub requires you to be authenticated in order to pull your image.
In OpenShift you can change the default pulling configuration so that it uses your token. You can do so as follows:

``` console
$ oc create secret docker-registry <SECRET_NAME> \
    --docker-server=docker.pkg.github.com \
    --docker-username=<YOUR_GITHUB_USERNAME> \
    --docker-password=<YOUR_GITHUB_PASSWORD>
$ oc secrets link default <SECRET_NAME> --for=pull \
    --namespace=<YOUR_OPENSHIFT_PROJECT_NAME>
```

## OpenShift

First you need to log in to your OpenShift cluster and its image registry:

``` console
$ docker login -u openshift -p $(oc whoami -t) <registry_ip>:<port>
$ oc login
$ oc project
Using project "inveniordm" on server "<registry_ip>:<port>".
```

Then, find your docker image and tag it with the url of your OpenShift registry:

``` console
$ docker images
REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
demo-inveniordm                                     latest              9b6dd5ae6b48        17 hours ago        2.33GB

$ docker tag demo-inveniordm <registry_ip>:<port>/inveniordm/demo-inveniordm:latest
```

!!! info "Project name"
    Note that `inveniordm` is the name of the OpenShift project we are using. Its value should be the one returned
    by the `oc project` command. Therefore the tag is: ``<registry_ip>:<port>/<project_name>/<name_of_your_image>:<version>``

Check that it was tagged correctly:

``` console
$ docker images                                                                   
REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
demo-inveniordm                                     latest              9b6dd5ae6b48        17 hours ago        2.33GB
<registry_ip>:<port>/inveniordm/demo-inveniordm     latest              9b6dd5ae6b48        17 hours ago        2.33GB
```

Finally push it to the image registry of OpenShift:

``` console
$ docker push <registry_ip>:<port>/inveniordm/demo-inveniordm:latest 
```

In order to use this image, you must set the following value in your `values.yaml` file (for both `web` and `worker`):

``` console
web:
    image: <registry_ip>:<port>/inveniordm/demo-inveniordm:rdm

worker:
    image: <registry_ip>:<port>/inveniordm/demo-inveniordm:rdm
```