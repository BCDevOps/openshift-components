# Setup
## Create the Jenkins Configuration
- copy xxx job configuration file and modify
  - jenkins.branch.BranchSource.id
  - repoOwner
  - repository
  - scriptPath

## Create secrets
Use the provided `openshift/secrets.json` as follow:
```
oc -n bcgov-tools process -f 'openshift/secrets.json' -p 'GH_USERNAME=' -p 'GH_PASSWORD=' | oc  -n bcgov-tools create -f -
```

## Grant Admin access to Jenkins Service account in each managed namespace
```
oc -n bcgov policy add-role-to-user 'admin' 'system:serviceaccounts:bcgov-tools:jenkins'
oc -n bcgov-tools policy add-role-to-group 'system:image-puller' 'system:serviceaccounts:bcgov'
```

# Build
```
( cd "$(git rev-parse --show-toplevel)" && .jenkins/pipeline-cli build --config=.jenkins/openshift/config.groovy --pr=19 )
```

# Deploy
```
( cd "$(git rev-parse --show-toplevel)" && .jenkins/pipeline-cli deploy --config=.jenkins/openshift/config.groovy --pr=19 --env=prod )
```
## Undeploy/Cleanup
```
oc -n bcgov-tools delete is/jenkins
```