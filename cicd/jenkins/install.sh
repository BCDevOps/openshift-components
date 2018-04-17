#!/usr/bin/env bash

read -p "Press enter to continue installing/updating Jenkins on '$(oc project -q)'"

oc delete all -l app=jenkins --ignore-not-found=true
oc delete all -l app=jenkins-pipeline --ignore-not-found=true
oc delete is/jenkins is/jenkins-2-rhel7 --ignore-not-found=true

oc import-image jenkins-2-rhel7:v3.7 --from=registry.access.redhat.com/openshift3/jenkins-2-rhel7:v3.7.42-2 --confirm
oc new-build jenkins-2-rhel7:v3.7~https://github.com/BCDevOps/openshift-components.git --context-dir=cicd/jenkins --name=jenkins
oc new-app jenkins-ephemeral -p NAMESPACE= -p JENKINS_IMAGE_STREAM_TAG=jenkins:latest --name=jenkins
oc set resources dc/jenkins --limits=cpu=2000m,memory=4Gi --requests=cpu=1000m,memory=1Gi
oc set volume dc/jenkins --remove --name=jenkins-data
oc set volume dc/jenkins --add --name=jenkins-jobs  -m /var/lib/jenkins/jobs -t pvc --claim-name=jenkins-jobs --claim-class=gluster-file --claim-mode=ReadWriteOnce --claim-size=1G --overwrite
