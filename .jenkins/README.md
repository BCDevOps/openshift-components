# Setup
## Create secrets
Use the provided `openshift/secrets.json` as follow:
```
oc -n bcgov-tools process -f 'openshift/secrets.json' -p 'GH_USERNAME=' -p 'GH_PASSWORD=' | oc  -n bcgov-tools create -f -
```

## Grant Admin access to Jenkins Service account in each managed namespace
```
oc -n bcgov policy add-role-to-user 'admin' 'system:serviceaccounts:bcgov-tools:jenkins'
```

# Build
```
cd "$(git rev-parse --show-toplevel)"
.jenkins/pipeline-cli build --config=.jenkins/openshift/config.groovy --pr=19
```

# Deploy
```
cd "$(git rev-parse --show-toplevel)"
.jenkins/pipeline-cli deploy --config=.jenkins/openshift/config.groovy --pr=19 --env=dev
```