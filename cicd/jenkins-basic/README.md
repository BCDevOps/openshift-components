Provides a basic/lightweight installation of Jenkins
- Does NOT provide support to OpenShift Pipeline integration
- Supports OpenShift Authentication


## How to Build:
```
( cd "$(git rev-parse --show-toplevel)" &&  .jenkins/pipeline-cli build --config=cicd/jenkins-basic/openshift/config.groovy --pr=19 )
```

## How to Deploy:
```
( cd "$(git rev-parse --show-toplevel)" && .jenkins/pipeline-cli deploy --config=cicd/jenkins-basic/openshift/config.groovy --pr=19 --env=prod )
```

## Hot to use it in your project
In or der to use this base image, you will need to layer your project jenkins configurations.
We recommend that the Jenkins configuration is stored in a folder called `.jenkins` at the root of your repository.
1. Create `.jenkins/docker/Dockerfile`
    ```
    FROM bcgov/jenkins-basic:v1-stable
    USER 0
    COPY ./contrib/jenkins/configuration $JENKINS_REF_HOME
    RUN set -x && \
        chgrp -R 0 $JENKINS_REF_HOME && \
        chmod -R 644 $JENKINS_REF_HOME && \
        chmod -R g+rwX $JENKINS_REF_HOME
    USER 1001
    ```
 1. Add your project's job configuration. For example, if your project/repository is called `hello-world`, add `.jenkins/docker/contrib/jenkins/configuration/jobs/hello-world/config.xml`
    ```xml
    <?xml version='1.1' encoding='UTF-8'?>
    <org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch@2.20">
      <actions/>
      <description></description>
      <properties>
        <org.csanchez.jenkins.plugins.kubernetes.KubernetesFolderProperty plugin="kubernetes@1.12.3">
          <permittedClouds/>
        </org.csanchez.jenkins.plugins.kubernetes.KubernetesFolderProperty>
      </properties>
      <folderViews class="jenkins.branch.MultiBranchProjectViewHolder" plugin="branch-api@2.0.20">
        <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
      </folderViews>
      <healthMetrics>
        <com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric plugin="cloudbees-folder@6.5.1">
          <nonRecursive>false</nonRecursive>
        </com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric>
      </healthMetrics>
      <icon class="jenkins.branch.MetadataActionFolderIcon" plugin="branch-api@2.0.20">
        <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
      </icon>
      <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy" plugin="cloudbees-folder@6.5.1">
        <pruneDeadBranches>true</pruneDeadBranches>
        <daysToKeep>-1</daysToKeep>
        <numToKeep>-1</numToKeep>
      </orphanedItemStrategy>
      <triggers/>
      <disabled>false</disabled>
      <sources class="jenkins.branch.MultiBranchProject$BranchSourceList" plugin="branch-api@2.0.20">
        <data>
          <jenkins.branch.BranchSource>
            <source class="org.jenkinsci.plugins.github_branch_source.GitHubSCMSource" plugin="github-branch-source@2.3.6">
              <id>08659502-ae8e-4300-a3b4-be5ec7fb9bd7</id>
              <credentialsId>github-account</credentialsId>
              <repoOwner>bcgov</repoOwner>
              <repository>hello-world</repository>
              <traits>
                <org.jenkinsci.plugins.github__branch__source.OriginPullRequestDiscoveryTrait>
                  <strategyId>2</strategyId>
                </org.jenkinsci.plugins.github__branch__source.OriginPullRequestDiscoveryTrait>
                <com.adobe.jenkins.disable__github__multibranch__status.DisableStatusUpdateTrait plugin="disable-github-multibranch-status@1.1"/>
                <jenkins.plugins.git.traits.WipeWorkspaceTrait plugin="git@3.9.1">
                  <extension class="hudson.plugins.git.extensions.impl.WipeWorkspace"/>
                </jenkins.plugins.git.traits.WipeWorkspaceTrait>
              </traits>
            </source>
            <strategy class="jenkins.branch.DefaultBranchPropertyStrategy">
              <properties class="empty-list"/>
            </strategy>
          </jenkins.branch.BranchSource>
        </data>
        <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
      </sources>
      <factory class="org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory">
        <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
        <scriptPath>Jenkinsfile</scriptPath>
      </factory>
    </org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>
    ```
    Make sure to update the following.
    1. `<id>08659502-ae8e-4300-a3b4-be5ec7fb9bd7</id>` by generating a random (uuid)[https://www.uuidgenerator.net/]
    2. `<repoOwner>bcgov</repoOwner>` and `<repository>hello-world</repository>`
    3. `<scriptPath>Jenkinsfile</scriptPath>`
    
    
## Copy update configuration files from a pod
```
oc -n agri-nmp-tools rsync jenkins-agri-nmp-10-lf4fp:/var/lib/jenkins/ $(git rev-parse --show-toplevel)/cicd/jenkins-basic/docker/contrib/jenkins/configuration --no-perms=true --exclude=.pki --exclude=.gnupg --exclude=jobs  --exclude=init.groovy.d --exclude=install.groovy.d --exclude=plugins --exclude=scripts.groovy.d --exclude=secrets  --exclude=.kube  --exclude=.cache --exclude=.java --exclude=monitoring  --exclude=users  --exclude=.groovy  --exclude=nodes --exclude=workflow-libs --exclude=logs --exclude=userContent --exclude=updates --exclude=builds --exclude=secret.key --exclude=secret.key.not-so-secret --exclude=credentials.xml --exclude=identity.key.enc  --exclude=jenkins.install.InstallUtil.lastExecVersion --exclude=queue.xml --exclude=.lastStarted --exclude=jenkins.model.JenkinsLocationConfiguration.xml --exclude=org.jenkinsci.plugins.github_branch_source.GitHubSCMProbe.cache --exclude=jenkins.telemetry.Correlator.xml

```