# Build your instance Docker image

In this section you will learn to build the docker image of your InvenioRDM instance! Doing so is as simple as running the following command:

``` console
docker build -t demo-inveniordm /path/to/your/instance --build-arg include_assets=true
```

!!! info "Tag name"
    In this case we have chosen to call our image `demo-inveniordm`, but you can choose your own name.

**Why is the `include_assets` flag needed**

When running InvenioRDM in local (`invenio-cli run`), you are running the uWSGI server on your own machine where you have built the statics. On the other hand, when running `invenio-cli containerize` you are building the docker image and then running it along the other containers. There, `invenio-cli` takes care of building the statics in the mounted volume for you. However, when building the image on your own (e.g. deploying somewhere else), you need to take care of the statics yourself.

This is the case when deploying in OpenShift. To solve this problem the chart defines a shared volume mounted on the Nginx and the Web containers.

When a volume is mounted it overwrites the contents of the folder (i.e. it will delete the assets). Therefore, we make use of an `initContainer` to mount the volume in a temporary location and copy to the volume the assets. This way when the volume is mounted into Nginx and Web containers it already has the assets. Being the end result that `/static` files can be served directly by Nginx.