[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# OpenShift Components

Useful components for day to day operations on OpenShift. 

## apps

Templates for build / deployment and useful support applications    

## cicd

Docker files to build Jenkins builder images

__Android__

This image contains OpenJSK >= 1.8.0 and the Android
SDK manager / tools for `gradle` builds. See the
Docker file for more precise version information.

__BDD Stack__

__Python3__

This image contains Python 3 and support tools like
`pip`.

__Python 3 & node.js 6.11__

This image contains Python 3 (with `pip`) and RedHat node.js 6.11 (with `npm`).

__node.js 6.11__ && __node.js 8.11__

This image contains __stock__ node.js 6.11 with the
latest `npm` (>= 6.0.0), `yarn`, and `nsp` cli tools installed
globally; see NODE_HOME to find installed components.

npm > 5.7.0 has the `ci` option that greatly increases
package install in a ci environment. Consider using it!

Image Reference
172.50.0.2:5000/openshift/jenkins-slave-node6:latest

__Sonar__

__Zap__

## db

Docker files to build data storage images

- **PostGIS** RHEL7 PostgreSQL 9.6 base image with PostGIS 2.4 extension(s). 

# How To

These images are manually built (and rebuild) when the Jenkins slave image
is updated. Contact your friendly neighbourhood DevOps lead if you need something
built or keep reading to do-it-yourself.

To build your own image, and add it to the registry, *but* keep it private to your
image stream(s) you can use the OpenShift `build.json` template in this repo
with the following command (make sure you're in tools ;) ):


```console
oc process -f build.json \
-p NAME=jenkins-slave-node \
-p OUTPUT_IMAGE_TAG=6 \
-p GIT_REPO_URL=https://github.com/BCDevOps/openshift-components.git \
-p SOURCE_CONTEXT_DIR=cicd/node6 | oc create -f -
```

| Parameter          | Optional      | Description   |
| ------------------ | ------------- | ------------- |
| NAME               | NO            | The name of your image |
| GIT_REPO_URL       | YES           | The location of the repository |
| SOURCE_CONTEXT_DIR | YES           | The path to the Dockerfile |

You normally dont need to change `GIT_REPO_URL` unless you've cloned the repo
and have added or changed Dockerfiles.

You can then check the Web GUI or use `oc get builds` to see the build progress.
When done you'll have a newly minted Docker image you can use; just reference
the image from your own image stream rather than OpenShift For example:

| Image Stream       | Reference   |
| ------------------ | ----------- |
| OpenShift          | `172.50.0.2:5000/openshift/jenkins-slave-node6` |
| Your Project       | `172.50.0.2:5000/mycool-project-tools/jenkins-slave-node6` |

