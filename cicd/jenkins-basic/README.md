Provides a basic/lightweight installation of Jenkins
- Does NOT provide support to OpenShift Pipeline integration
- Supports OpenShift Authentication


## How to Build:
```
cd "$(git rev-parse --show-toplevel)"
.jenkins/pipeline-cli --config=cicd/jenkins-basic/openshift/config.groovy --pr=19
```

## How to Deploy:
```
cd "$(git rev-parse --show-toplevel)"
.jenkins/pipeline-cli deploy --config=cicd/jenkins-basic/openshift/config.groovy --pr=19 --env=dev
```