import hudson.model.*
import jenkins.model.Jenkins
import jenkins.security.s2m.AdminWhitelistRule
import org.jenkinsci.plugins.workflow.job.WorkflowJob;
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition;
import hudson.plugins.git.GitSCM;
import hudson.plugins.git.BranchSpec;
import java.util.UUID;
import java.net.URL;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import org.jenkinsci.plugins.scriptsecurity.scripts.ScriptApproval
//import org.jenkinsci.plugins.scriptsecurity.scripts.languages.GroovyLanguage
import hudson.util.Secret;

def runOrDie(command, String errorMessage){
    def process=command.execute()
    System.err.println(command)
    String processText = process.text
    def exitValue = process.waitFor()
    if (process.exitValue() != 0 ) throw new RuntimeException("${errorMessage} (exit value:${process.exitValue()})")
    return processText
}

final ScriptApproval scriptApproval = ScriptApproval.get();

println("jenkins-init-00:Binding Variables:")

binding.variables.each{
    println it.key
    println it.value
}

println("jenkins-init-00:jenkinsConfig:${jenkinsConfig}")




println 'Configuring JNLP agent protocols'
//https://github.com/samrocketman/jenkins-bootstrap-shared/blob/master/scripts/configure-jnlp-agent-protocols.groovy
Jenkins.instance.setAgentProtocols(['JNLP4-connect', 'Ping'] as Set<String>)
Jenkins.instance.save()

//https://github.com/samrocketman/jenkins-bootstrap-shared/blob/master/scripts/configure-csrf-protection.groovy
println 'Configuring CSRF protection'
Jenkins.instance.setCrumbIssuer(new hudson.security.csrf.DefaultCrumbIssuer(true))
Jenkins.instance.save()

println 'Configuring Slave to Master Access Control'
//https://github.com/samrocketman/jenkins-bootstrap-shared/blob/master/scripts/security-disable-agent-master.groovy
//https://wiki.jenkins.io/display/JENKINS/Slave+To+Master+Access+Control
Jenkins.instance.getInjector().getInstance(AdminWhitelistRule.class).setMasterKillSwitch(false)
Jenkins.instance.save()


if (jenkinsConfig['github-webhook']!=null && jenkinsConfig['github-webhook']?.job?.name != null) {
    Map jobCfg=jenkinsConfig['github-webhook']?.job
    String jobName=jobCfg.name

    println "Creating '${jobName}' job"
    String ghPushJobConfigXml = new URL(jobCfg.template.source).getText(StandardCharsets.UTF_8.name()).trim();
    for (Map param:jobCfg.template.parameters){
        ghPushJobConfigXml = ghPushJobConfigXml.replaceAll(java.util.regex.Pattern.quote("#{${param.name}}"), param.value);
    }

    if (Jenkins.instance.getItem(jobName) == null) {
        InputStream ghPushJobConfigInputStream = new ByteArrayInputStream(ghPushJobConfigXml.getBytes(StandardCharsets.UTF_8));
        Jenkins.instance.createProjectFromXML(jobName, ghPushJobConfigInputStream);
    }


    for (Object builder : Jenkins.instance.getItem(jobName).getBuilders()) {
        if (builder instanceof hudson.plugins.groovy.SystemGroovy) {
            ScriptApproval.PendingScript s = new ScriptApproval.PendingScript(builder.source.script.script, org.jenkinsci.plugins.scriptsecurity.scripts.languages.GroovyLanguage.get(), org.jenkinsci.plugins.scriptsecurity.scripts.ApprovalContext.create())
            scriptApproval.approveScript(s.getHash())
        }
    }
    def userCfg=jenkinsConfig['github-webhook']?.user

    if (userCfg!=null && userCfg['secret.name'] !=null ) {

        String jobUsername = runOrDie(['sh', '-c', 'oc get secret/' + userCfg['secret.name'] + ' --template={{.data.username}} | base64 --decode'], "'secret/"+userCfg['secret.name']+"' was NOT found")
        String jobPassword = runOrDie(['sh', '-c', 'oc get secret/' + userCfg['secret.name'] + ' --template={{.data.password}} | base64 --decode'], "'secret/"+userCfg['secret.name']+"' was NOT found")

        User u = User.get(jobUsername)
        println "username:${u.getId()}"
        def apiToken=u.getProperty(jenkins.security.ApiTokenProperty.class)
        apiToken.apiToken=Secret.fromString(jobPassword)

        println "\'github-webhook\' API token:${u.getProperty(jenkins.security.ApiTokenProperty.class).getApiTokenInsecure()}"

        Jenkins.instance.getAuthorizationStrategy().add(Jenkins.READ, jobUsername)
        Jenkins.instance.getAuthorizationStrategy().add(Item.BUILD, jobUsername)
        Jenkins.instance.getAuthorizationStrategy().add(Item.DISCOVER, jobUsername)
        Jenkins.instance.getAuthorizationStrategy().add(Item.READ, jobUsername)
    }

    Jenkins.instance.save()
}

/*
def jenkins = Jenkins.getInstance()
User u = User.get("github-webhook")
println "username:${u.getId()}"
println "\'github-webhook\' API token:${u.getProperty(jenkins.security.ApiTokenProperty.class).getApiTokenInsecure()}"

jenkins.getAuthorizationStrategy().add(Jenkins.READ, "github-webhook")
jenkins.getAuthorizationStrategy().add(Item.BUILD, "github-webhook")
jenkins.getAuthorizationStrategy().add(Item.DISCOVER, "github-webhook")
jenkins.getAuthorizationStrategy().add(Item.READ, "github-webhook")
*/

println 'Approving script signatures'
def signatures=new XmlSlurper().parseText('''
<signature>
    <string>method hudson.model.AbstractItem updateByXml javax.xml.transform.stream.StreamSource</string>
    <string>method hudson.model.ItemGroup getItem java.lang.String</string>
    <string>method hudson.plugins.git.GitSCM getBranches</string>
    <string>method hudson.plugins.git.GitSCM getRepositories</string>
    <string>method hudson.plugins.git.GitSCM getUserRemoteConfigs</string>
    <string>method hudson.plugins.git.GitSCMBackwardCompatibility getExtensions</string>
    <string>method hudson.scm.SCM getBrowser</string>
    <string>method java.io.BufferedReader readLine</string>
    <string>method java.lang.AutoCloseable close</string>
    <string>method java.lang.String getBytes java.nio.charset.Charset</string>
    <string>method jenkins.model.Jenkins createProject java.lang.Class java.lang.String</string>
    <string>method jenkins.model.ModifiableTopLevelItemGroup createProjectFromXML java.lang.String java.io.InputStream</string>
    <string>new java.io.BufferedReader java.io.Reader</string>
    <string>new java.io.ByteArrayInputStream byte[]</string>
    <string>new javax.xml.transform.stream.StreamSource java.io.InputStream</string>
    <string>staticField java.nio.charset.StandardCharsets UTF_8</string>
    <string>staticMethod jenkins.model.Jenkins getInstance</string>
    <string>method java.lang.String indexOf java.lang.String int</string>
    <string>new java.io.PrintWriter java.io.Writer</string>
    <string>method java.lang.Throwable printStackTrace java.io.PrintWriter</string>
</signature>''');

signatures.string.each {
    scriptApproval.approveSignature(it.text());
}


