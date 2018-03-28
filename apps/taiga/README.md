###Provision a PostGres database

```bash
oc process -n openshift postgresql-persistent -p POSTGRESQL_USER=taiga -p POSTGRESQL_DATABASE=taiga -p POSTGRESQL_PASSWORD=<postgres_pwd> -p VOLUME_CAPACITY=250Mi | oc apply  -n <deployment namespace> -f -
```

###Configure taiga-front build 

```bash
oc process -f taiga-front-bc.json | oc apply -n <tools namespace> -f -
```

###Configure taiga-back build elements

```bash
oc process -f taiga-back-bc.json | oc apply -n <tools namespace> -f -
```

###Deploy taiga-front

```bash
oc process -f taiga-front-deployment.json -p ROUTE_URL=<route> -p TAIGA_API_URL=https://<backend-route>/api/v1/ -p GITHUB_CLIENT_ID=<git client id> | oc apply -n <deployment namespace> -f -
```

###Deploy taiga-back

```bash
oc process -f taiga-back-deployment.json -p FROM_EMAIL=<email> -p EMAIL_HOST=<email host> -p DATABASE_PASSWORD=<db pwd> -p GITHUB_API_CLIENT_SECRET=<github secret> -p GITHUB_API_CLIENT_ID=<github client id> -p TAIGA_FRONT_DOMAIN=<front route> -p ROUTE_URL=<backend route> | oc apply -n <deployment namespace> -f -
```

###Create admin user 
```bash
python manage.py adminusercreate --username admin --password <password>
```

###Load project templates
```bash
python manage.py loaddata initial_project_templates
```
