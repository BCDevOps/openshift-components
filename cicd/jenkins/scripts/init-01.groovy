import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.domains.*;
import org.jenkinsci.plugins.plaincredentials.impl.*;
import hudson.util.Secret;
import jenkins.model.*;
import hudson.model.*;
import java.net.URL;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import com.openshift.jenkins.plugins.OpenShiftTokenCredentials;


def runOrDie(command, String errorMessage){
  def process=command.execute()
  String processText = process.text
  def exitValue = process.waitFor()
  if (process.exitValue() != 0 ) throw new RuntimeException("${errorMessage} (exit value:${process.exitValue()})")  
  return processText
}

println "Initializing from remote script"
String jenkinsConfigText = runOrDie(['oc', 'get', 'configmaps/jenkins', '--template={{.data.config}}'], "'ConfigMaps/jenkins' was NOT found")
String githubUsername=runOrDie(['sh', '-c', 'oc get secret/github-credentials --template={{.data.username}} | base64 --decode'], "'secret/github-credentials' was NOT nound")
String githubPassword=runOrDie(['sh', '-c', 'oc get secret/github-credentials --template={{.data.password}} | base64 --decode'], "'secret/github-credentials' was NOT nound")
def jenkinsConfig = new groovy.json.JsonSlurper().parseText(jenkinsConfigText?:'{}')

println "Jenkins ConfigMap:"
println "${jenkinsConfig}"


/* TODO:
- Create Jenkins Credetential "Secret Text" with id "github-access-token"
- Create Jenkins Credential "Username and Password" with id "github-account" where password is the same as "github-access-token"
- Setup GitHub Server using the "github-access-token" credential
  - uncheck "Manage Hooks"
*/

/* LOGGER:
org.jenkinsci.plugins.workflow.multibranch
org.jenkinsci.plugins.github_branch_source
jenkins.branch
hudson.plugins.git
org.jenkinsci.plugins.github

*/



/*
method hudson.plugins.git.UserRemoteConfig getUrl
method hudson.scm.SCM getKey
method org.jenkinsci.plugins.workflow.support.steps.build.RunWrapper getRawBuild
method hudson.model.Run getPreviousBuildInProgress

*/

Credentials c1 = (Credentials) new UsernamePasswordCredentialsImpl(
  CredentialsScope.GLOBAL,
  "github-account",
  "GitHub account",
  githubUsername,
  githubPassword);

SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c1);

Credentials c2 = (Credentials) new StringCredentialsImpl(
   CredentialsScope.GLOBAL,
  "github-access-token",
  "GitHub account (Access Token)",
  Secret.fromString(githubPassword));

SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), c2);


def jsonSlurper = new groovy.json.JsonSlurper()
def deployerCredentials = jsonSlurper.parseText(['sh', '-c', 'oc get secret/jenkins-deployer-credentials -o json'].execute().text)
deployerCredentials.data.each { key, value ->
  Credentials cred = (Credentials) new OpenShiftTokenCredentials(
          CredentialsScope.GLOBAL,
          "jenkins-deployer-"+key,
          "OpenShift Secret (${key})",
          Secret.fromString(new String(value.decodeBase64())));

  SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), cred);
}

println "Configuring GitHub API"
Jenkins.getInstance().getDescriptor(org.jenkinsci.plugins.github.config.GitHubPluginConfig.class)
def ghCofigs = Jenkins.getInstance().getDescriptor(org.jenkinsci.plugins.github.config.GitHubPluginConfig.class).getConfigs();
def ghServerConfig = new org.jenkinsci.plugins.github.config.GitHubServerConfig('github-access-token');
ghServerConfig.setName('GitHub')
ghServerConfig.setApiUrl('https://api.github.com')
ghServerConfig.setManageHooks(false);
ghServerConfig.setClientCacheSize(21)
ghCofigs.clear();
ghCofigs.add(ghServerConfig);


if (jenkinsConfig.globalLibraries) {
  println "Configuring Global Libraries"
  List libraries=[]
  for (Map globalLibrary: jenkinsConfig.globalLibraries) {
    def libScm = new jenkins.plugins.git.GitSCMSource(globalLibrary.scm.url);
    libScm.setCredentialsId('github-account');
    libScm.setTraits([new jenkins.plugins.git.traits.BranchDiscoveryTrait(), new jenkins.plugins.git.traits.TagDiscoveryTrait()]);
    def libRetriever = new org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever(libScm)
    def libConfig = new org.jenkinsci.plugins.workflow.libs.LibraryConfiguration(globalLibrary.name, libRetriever)
    libConfig.setDefaultVersion(globalLibrary.defaultVersion?:'master');
    libConfig.setImplicit(globalLibrary.implicit?:true);
    libConfig.setAllowVersionOverride(globalLibrary.allowVersionOverride?:true);
    libConfig.setIncludeInChangesets(globalLibrary.includeInChangesets?:true);
    libraries.add(libConfig)
  }

  Jenkins.getInstance().getDescriptor(org.jenkinsci.plugins.workflow.libs.GlobalLibraries.class).setLibraries(libraries)
  Jenkins.getInstance().save()
}



if (jenkinsConfig.projects) {
  println "Loading Projects"
  jenkinsConfig.projects.each { String projectName, Map projectCfg ->
    println "Loading Project '${projectName}' from  '${projectCfg.template.source}'"
    String configXml = new URL(projectCfg.template.source).getText(StandardCharsets.UTF_8.name()).trim();
    for (Map param:projectCfg.template.parameters){
      configXml = configXml.replaceAll(java.util.regex.Pattern.quote("#{${param.name}}"), param.value);
    }
    InputStream configXmlInputStream = new ByteArrayInputStream(configXml.getBytes(StandardCharsets.UTF_8));
    Jenkins.instance.createProjectFromXML(projectName, configXmlInputStream);
  }
  Jenkins.getInstance().save()
}

def sa = org.jenkinsci.plugins.scriptsecurity.scripts.ScriptApproval.get();
[
  'method hudson.plugins.git.UserRemoteConfig getUrl',
  'method hudson.scm.SCM getKey',
  'method org.jenkinsci.plugins.workflow.support.steps.build.RunWrapper getRawBuild',
  'method hudson.model.Run getPreviousBuildInProgress',
  'staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods putAt java.lang.Object java.lang.String java.lang.Object'
].each {
  sa.approveSignature(it);
}


String jenkinsRouteHost = ['sh', '-c', 'oc get route/jenkins --template={{.spec.host}}'].execute().text.trim()
JenkinsLocationConfiguration.get().setUrl("https://${jenkinsRouteHost}/")
