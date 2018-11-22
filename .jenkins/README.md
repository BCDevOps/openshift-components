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



oc -n bcgov-tools process -f 'openshift/secrets.json' -p 'GH_USERNAME=cvarjao' -p 'GH_PASSWORD=b3fb0f340e2b31281aadfbe4cc3201c33d67707d' | oc  -n bcgov-tools create -f -

# Build
```
.jenkins/pipeline-cli --config=.jenkins/openshift/config.groovy --pr=19
```

# Deploy
```
.jenkins/pipeline-cli --config=.jenkins/openshift/config.groovy --pr=19 --env=dev
```