#!/usr/bin/env bash

oc import-image jenkins-2-rhel7:v3.7 --from=registry.access.redhat.com/openshift3/jenkins-2-rhel7:v3.7.42-2 --confirm
oc new-build jenkins-2-rhel7:v3.7~https://github.com/BCDevOps/openshift-components.git --context-dir=cicd/jenkins --name=jenkins

