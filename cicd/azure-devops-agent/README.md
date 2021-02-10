
# TL;DR

This builder image runs the Azure DevOps agent to connect to the Azure DevOps control plane for creating and managing builds and deployments. Out of the box, the following build tools are included:

- .Net Core     v2.2 
- OpenJDK       v1.8.0
- node.js       v10.13

# Warning

There are bugs in .net core 2.2 that cause authentication negotiation to fail when using Kerberos, NTLM, or Basic Auth. Basic Auth header will work though. Fixes are in .net core 3.0 which, at the time of writing this, is still in beta. Its recommended to use ADFS authentication which aligns with cloud native development. 

# Known Issues

There is a permissions problem that prevents the agent from updating itself when a new version is available.

# Builder Image

Create a builder image. This will be the image that runs the agent and waits for work. The OpenShift Container Platform (OCP) manifest below will build the image and create an image stream to store the newly minted image. While you don't need to change any parameters to get this working you can explore the parameters for customizations.

```console
oc process -f https://raw.githubusercontent.com/jleach/openshift-components/master/cicd/azure-devops-agent/openshift/build.yaml | oc apply -f -
```

# Run

Its best to create an deployment config with the params you want so that the image will restart properly and be managed by OCP. To do a quick test run you can use the command below. Replace `blabla-tools` with your tools namespace; and use `oc project` to make sure you're in the correct namespace before you run the command. It will use the Jenkins service account to ensure that it has the proper permissions to to act as a builder.

```console
oc run az-image --image=docker-registry.default.svc:5000/blabla-tools/azure-develop-agent:v2.153.2  --replicas=1 --restart=Never --env="AZ_DEVOPS_ORG_URL=$AZ_DEVOPS_ORG_URL" --env="AZ_DEVOPS_TOKEN=$AZ_DEVOPS_TOKEN" --requests="cpu=1,memory=1Gi" --limits="cpu=1,memory=1Gi" --serviceaccount=jenkins
```

Once run, the agent will come on-line and appear in the `default` pool with the name `az-image`.

# Deploy

Create your deployment script loosely based on the `Run` example above. There are other options you can pass as environment variables. See the [startup script](https://raw.githubusercontent.com/jleach/openshift-components/master/cicd/azure-devops-agent/scripts/start.sh) for more details.

You'll need to deploy it using the Jenkens service account or create your own service account with similar privileges so that it can update image streams.

To trigger an `s2i` build on OCP you can package up the artifacts and inject them into an image build. The `azure-pipelines.yml` example below checks-out the source code; installs the tools (npm); runs the automated tests; and finally packages up the source (excluding node_modules) and injects it into an s2i build that bakes the image:

```
# Node.js
# Build a general Node.js project with npm.
# Add steps that analyze code, save build artifacts, deploy, and more:
# https://docs.microsoft.com/azure/devops/pipelines/languages/javascript
#

trigger:
- master

# Specify your pool here if the agent is not part of `Default`
# pool:
#   vmImage: 'ubuntu-latest'

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '10.x'
  displayName: 'Install Node.js'

- script: |
    npm ci
    CI=true npm run test
  displayName: 'npm install and test'

- script: |
    tar --exclude='./node_modules' -cf artifact.tar .
    oc start-build mybuild-api-build --from-archive=artifact.tar --follow --wait
  displayName: 'start s2i build'
  condition: ne(variables['Build.Reason'], 'PullRequest')
```