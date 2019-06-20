#! /bin/bash
#
# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Created by Jason Leach on 2019-06-20
#

set -Eeo pipefail

# =================================================================================================================
# Usage:
# -----------------------------------------------------------------------------------------------------------------
usage() {
  cat <<-EOF
  A helper script configure and start the Azure DevOps Agent.

  Usage: ${0} [ -h -x -r <OpenShiftRegistryAddress>] -i <ImageName> -n <OpenShiftProjectNamespace> ]

  OPTIONS:
  ========
    -u The Azure DevOps Organization URL.
       Example `https://fullboar.visualstudio.com`
    -t The Personal Access Token (PAT) for this Agent.
       Example `kd2kdkj2ojldkajdf4jr938jf9edjsdkfjdfj20e`
    -n Optional. The name of the Agent.
       Defaults to hostname.
       Example `d0e46b5cde65`
    -p Optional.  The name of the pool you would like this
       agent to belong to.
       Defaults to `default`

    -h prints the usage for the script
    -x run the script in debug mode to see what's happening

EOF
exit
}

# -----------------------------------------------------------------------------------------------------------------
# Initialization:
# -----------------------------------------------------------------------------------------------------------------
while getopts u:t:n:p:hx FLAG; do
  case $FLAG in
    u ) export AZ_DEVOPS_ORG_URL=$OPTARG ;;
    t ) export AZ_DEVOPS_TOKEN=$OPTARG ;;
    n ) export AZ_DEVOPS_AGENT_NAME=$OPTARG ;;
    p ) export AZ_DEVOPS_POOL=$OPTARG ;;
    x ) export DEBUG=1 ;;
    h ) usage ;;
    \? ) #unrecognized option - show help
      echo -e \\n"Invalid script option: -${OPTARG}"\\n
      usage
      ;;
  esac
done

# Shift the parameters in case there any more to be used
shift $((OPTIND-1))

if [ ! -z "${DEBUG}" ]; then
  set -x
fi

if [ -z "${AZ_DEVOPS_ORG_URL}" ] || [ -z "${AZ_DEVOPS_TOKEN}" ]; then
  echo -e \\n"Missing parameters. Organization URL and Token are required."\\n
  usage
fi

pushd $(dirname $0)/agent

source ./env.sh

./bin/Agent.Listener configure --unattended \
    --agent "${AZ_DEVOPS_AGENT_NAME:-$(cat /proc/sys/kernel/hostname)}" \
    --url "${AZ_DEVOPS_ORG_URL}" \
    --auth PAT \
    --token $AZ_DEVOPS_TOKEN \
    --pool "${AZ_DEVOPS_POOL:-default}"\
    --work "$(dirname $0)/_work" \
    --replace & wait $!

./bin/Agent.Listener run & wait $!

