## Hot to use it in your project
In or der to use this base image, you will need to layer your project jenkins configurations.
We recommend that the Jenkins configuration is stored in a folder called `.jenkins` at the root of your repository.
1. Create a secret for GitHub credentials:
    ```
    oc -n <namespace> -f 'openshift/deployment-prereq.yaml' -p 'GH_USERNAME=<username>' -p 'GH_PASSWORD=<token>' | oc  -n <namespace> create -f -
    ```
    1. update `<namespace>` to be your project `-tools` namespace
    1. update `<username` to be the account used for connecting to GitHub. Please create a [user/bot account](https://help.github.com/en/articles/differences-between-user-and-organization-accounts) for the team.
    1. update `<token>` to be the generated [Personal Access Token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) for `<username>`. The koen needs to have the following privilege: `repo:status`, `repo_deployment`, and `public_repo`.
1. Create `.jenkins/docker/Dockerfile`

    see example of this file in [docker/Dockerfile](./docker/Dockerfile)
1. Add your project's job configuration. For example, if your project/repository is called `hello-world`, add `.jenkins/docker/contrib/jenkins/configuration/jobs/hello-world/config.xml`

    seet example of this file in docker/contrib/jenkins/configuration/jobs/hello-world/config.xml
    Make sure to update the following.
    1. `<id>08659502-ae8e-4300-a3b4-be5ec7fb9bd7</id>` by generating a random (uuid)[https://www.uuidgenerator.net/]
    2. `<repoOwner>bcgov</repoOwner>` and `<repository>hello-world</repository>`
    3. `<scriptPath>Jenkinsfile</scriptPath>`
    
    
