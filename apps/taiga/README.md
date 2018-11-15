---

title: "Taiga for OpenShift"
description: "A set of resources and customizations to deploy Taiga on BC Gov OpenShift."

---

# Taiga for OpenShift

## Intro

### What is Taiga?

Taiga is an open source agile collaboration/project management tool built using Django.  It was loosely based on the older Redmine collaboration tool.  It provides basic ticket/issue tracking as well as supporting common Agile/Scrum constructs.tools such as User Stories, Epics, Sprints, and Kanban boards, More info on functionality can be found [here](https://taiga.io).  Info about the architecture and deployment of the open source distribution can be found [here](http://taigaio.github.io/taiga-doc/dist/).  We have based our work on building and deployment largely on the latter. 

The Taiga's configuration that is contained in this repo includes Taiga's [optional GitHub authentication plugin](https://github.com/taigaio/taiga-contrib-github-auth) and a small extension that we have implemented which enforces membership in a configurable GitHub organization.  This can be disabled and username/password authentication can be used instead, but documentation is an "undocumented capability" at the moment.

### Known Issues/Limitations

The Taiga configuration in this repo utilizes GitHub registration and authentication.  There are two "gotchas" (actually one gotcha and one...bug) related to this: 

* Users attempting to register and subsequently login *must* be ***public*** members of the configured GitHub organization.  This is not the default membership, so users will need to change this in order to be able to register or login to Taiga.
* For the project invitation feature, the email of the invitee must match ***exactly*** the email address associated with their GitHub ID

One more "thing to know" related to security:

* The file attachments feature generates cryptic/hard to guess links for attachments, but it ***does not restrict access to attachments***.  For example if a file is attached to an issue in a private Taiga project, a cryptic link would be generated for the attachment but would technically be accessible to anyone who had or could infer the link.  This is a common approach in some Dropbox-like tools but teams should satisfy themselves that this is appropriate/sufficient for the sensitivity of material they are storing in Taiga.  

### What is in this repo?

In this repo, we have created a set of artifacts (json templates) that build Taiga images and deploy them into an OpenShift environment.

Architecturally, Taiga consists of a Postgres database, a Django-based API, and an AngularJS frontend. Instructions are provided below on provisioning a Postgres instnace using an OpenShfit provided template.  There are build and deployment artifacts in this repo for the API (aka `back`) the frontend (aka `front`) components and this document provides instructions on how to use them.

Note: **BCGov users will not need to build Taiga** as ImageStreams are provided in the global `openshift` namespace.    

### Requirements and Assumptions

* In order to make use of the artifacts provided here, you must have access to an OpenShift Container Platform instance.

* You will need a project space within OpenShift and "write" access to it. (For BCGov projects, we recommend that you run Taiga in a "tools" project)

* You also need the `oc` command line tool.

* You will need to create an OAuth app in GitHub as the client ID and secret are required for the Taiga GitHub aith plugin.  OAuth apps at the organization level are confirmed working.  User level OAuth apps have not been tested, but should also work.  The "Authorization callback URL" in GitHub should be look like: `https://<your taiga frontend url>/login`, where `<your taiga frontend url>` matches the value you will provide as `ROUTE_URL` when you deploy the frontend below.

* It is assumed that you want to run all of Taiga's components in the same OpenShift project space

* It is assumed that you will have a dedicated PostgreSQL instance for Taiga   


## Deployment

Assuming you *do not* need to build Taiga images/ImageStream (this is true for BC Gov users), you can just follow the steps below to deploy an instance in your project space.

1. Provision a PostgreSQL database

    This step stands up a PostgreSQL instance which Taiga uses to store its data.
    
    ### Parameters:
    
    | Parameter Name | Purpose | Note |
    | --- | --- | --- |
    | POSTGRESQL_PASSWORD | sets the password for the PostgreSQL instance you are deploying | You can also omit this parameter and a password will be generated.  Either way, this value is needed in a subsequent step, so you'll either need to make a note of the value you provide, or you can dig it out from a secret afterwards (Google is your friend).|
       
    If you choose, you can also provide a different value for `VOLUME_CAPACITY` or any of the other parameters the template provides.

    ```bash
    oc process -n openshift postgresql-persistent -p POSTGRESQL_USER=taiga -p POSTGRESQL_DATABASE=taiga -p POSTGRESQL_PASSWORD=<postgres_pwd> -p VOLUME_CAPACITY=250Mi | oc apply  -n <deployment namespace> -f -
    ```

1. Deploy taiga-back

    This step stands up the Django component tha Taiga uses as its API server.  
    
    ### Parameters:
        
    | Parameter Name | Purpose | Note |
    | --- | --- | --- |    
    | IMAGESTREAM_TAG | The version of Taiga you would like to deploy.  | This value actually correspond to a "tag" used on the Taiga image/ImageStream, and the tag must exist.  At the time of this writing the newest version is 3.3.8.  Note that updates to the image version are not automatic, meaning that there is a build step that must be performed by the DevOps platform team. |
    | FROM_EMAIL | The email address that Taiga will use as its "from" value when sending outbound emails such as notifications. | |
    | EMAIL_HOST | The SMTP host that Taiga should use to send outbound email.  | |
    | DATABASE_PASSWORD | The password for the PostgreSQL instance created in the prior deployment step. | This will be stored as a `secret` and be made available to the Taiga container at runtime.  |
    | GITHUB_API_CLIENT_SECRET | The GitHub client secret associated with the OAuth app you've configured in GitHub. | |
    | GITHUB_API_CLIENT_ID | The GitHub client ID associated with the OAuth app you've configured in GitHub. | | 
    | TAIGA_FRONT_DOMAIN | The fully qualified domain name bit of the URL where the Taiga `front` component will listen. | The is needed by the backend to generate absolute URL links. |
    | ROUTE_URL |The fully qualified domain name bit of the URL where the Taiga `back` component will listen.   | This is used to create the `route` object in OpenShift.  |
    | TAIGA_GITHUB_EXTENDED_AUTH_ORG | The GitHub organization that users must be a member of.  | |
                        
    ```bash
    oc process -f taiga-back-deployment.json -p IMAGESTREAM_TAG=<taiga version> -p FROM_EMAIL=<email> -p EMAIL_HOST=<email host> -p DATABASE_PASSWORD=<db pwd> -p GITHUB_API_CLIENT_SECRET=<github secret> -p GITHUB_API_CLIENT_ID=<github client id> -p TAIGA_FRONT_DOMAIN=<front route> -p ROUTE_URL=<backend route> -p TAIGA_GITHUB_EXTENDED_AUTH_ORG=BCDevOps | oc apply -n <deployment namespace> -f -
    
    ```

1. Deploy taiga-front

    This step stands up the pod that uses `caddy` to serve up the Taiga frontend AngularJS app to clients.  

    | Parameter Name | Purpose | Note |
    | --- | --- | --- |  
    | ROUTE_URL | The fully qualified domain name bit of the URL where the Taiga `front` component will listen. |  This is used to create the `route` object in OpenShift |
    | IMAGESTREAM_TAG |The version of Taiga you would like to deploy.  | This value actually corresopnd to a "tag" used on the Taiga image/ImageStream, and the tag must exist.  At the time of this writing the newest version is 3.3.8.  Note that updates to the image version are not automatic, meaning that there is a build step that must be performed by the DevOps platform team. | 
    | TAIGA_API_URL | The fully qualified domain name bit of the URL where the Taiga `back` component listens for API calls from the frontend. | 
    | GITHUB_CLIENT_ID | The GitHub client ID associated with the OAuth app you've configured in GitHub. | This is required for the GitHub authentication plugin. |    

    ```bash
    oc process -f taiga-front-deployment.json -p IMAGESTREAM_TAG=<taiga version> -p ROUTE_URL=<route> -p TAIGA_API_URL=https://<backend-route>/api/v1/ -p GITHUB_CLIENT_ID=<git client id> | oc apply -n <deployment namespace> -f -
    ```

1. Create admin user 

    This step will create the initial `admin` user for Taiga.  
    
    The admin user you create can login to the Django admin Web UI as well as the Taiga frontend.
    
    The Django admin UI will be at https://<TAIGA_API_URL>/admin/.

    ```bash
    oc rsh $(oc get pods --no-headers -l name=taiga-back | awk '{print $1}' ) # the magic to the left will drop you into a shell inside your pod running the Taiga back Django app. You'll run the command below from this shell.   
    python manage.py adminusercreate --username <admin username you choose> --password <password you choose>
    ```

1. Load project templates

    This step will seed Taiga with some data structures needed in order to create new project instances, etc. 

    ```bash
    oc rsh $(oc get pods --no-headers -l name=taiga-back | awk '{print $1}' ) # the magic to the left will drop you into a shell inside your pod running the Taiga back Django app. You'll run the command below from this shell.
    python manage.py loaddata initial_project_templates
    
    ```
## Building ImageStreams for Taiga - ***Advanced***  - 

If you just want to deploy Taiga, then this section is TL;DR and you can just follow the steps above. 

If you're still reading, the steps below describe what you need in order to set up the build configurations to build a set of Taiga ImageStreams that can subsequently be deployed using the approach described in the Deployment section of this document. 

The result will be several images/ImageStreams with a deployable image/ImageStream for each of the `front` and `back` components of Taiga. 

###Configure taiga-back build elements

```bash
oc process -f taiga-back-bc.json | oc apply -n <tools namespace> -f -
```

###Configure taiga-front build 

```bash
oc process -f taiga-front-bc.json | oc apply -n <tools namespace> -f -
```

