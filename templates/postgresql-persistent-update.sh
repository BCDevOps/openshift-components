#!/usr/bin/env sh

################################################################################
#  Fetching Source
################################################################################

oc -n openshift create -f https://raw.githubusercontent.com/sclorg/postgresql-container/28de1f11c9124a7c2c0f341c5606073cf3c7dab2/examples/postgresql-persistent-template.json --dry-run=true -o json > postgresql-persistent.json

################################################################################
#  Customizations
################################################################################

# Set spec.storageClassName to 'gluster-file-db'
cp postgresql-persistent.json postgresql-persistent.input.json
jq '.objects[2].metadata += {"annotations":{"volume.beta.kubernetes.io/storage-provisioner": "kubernetes.io/glusterfs"}} | .objects[2].spec += {"storageClassName": "gluster-file-db"}' postgresql-persistent.input.json > postgresql-persistent.json

# set .annotations["volume.beta.kubernetes.io/storage-provisioner"] to "kubernetes.io/glusterfs"
cp postgresql-persistent.json postgresql-persistent.input.json
jq '.objects[2].metadata += {"annotations":{"volume.beta.kubernetes.io/storage-provisioner": "kubernetes.io/glusterfs"}}' postgresql-persistent.input.json > postgresql-persistent.json

#clean up temporary file
rm postgresql-persistent.input.json
