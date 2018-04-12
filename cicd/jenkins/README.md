# s2i-jenkins

```

#import jenkins base image and create ImageStream
oc import-image jenkins-2-rhel7:v3.7 --from=registry.access.redhat.com/openshift3/jenkins-2-rhel7:v3.7 --confirm

oc new-build jenkins-2-rhel7:v3.7~https://github.com/cvarjao/openshift-components.git --context-dir=cicd/jenkins --name=jenkins
oc new-app jenkins-ephemeral -p NAMESPACE= -p JENKINS_IMAGE_STREAM_TAG=jenkins:latest --name=jenkins

oc set resources dc/jenkins --limits=cpu=2000m,memory=4Gi --requests=cpu=1000m,memory=1Gi

#Configuring mount/volume
oc set volume dc/jenkins --remove --name=jenkins-data
oc set volume dc/jenkins --add --name=jenkins-jobs  -m /var/lib/jenkins/jobs -t pvc --claim-name=jenkins-jobs --claim-class=gluster-file --claim-mode=ReadWriteOnce --claim-size=1G --overwrite



```


# References:

- https://github.com/openshift/jenkins
- https://github.com/jenkinsci/github-plugin/blob/master/src/main/java/com/cloudbees/jenkins/GitHubWebHook.java
- https://github.com/jenkinsci/build-token-root-plugin/pull/16
