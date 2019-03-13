## Hot to use it in your project
In or der to use this base image, you will need to layer your project jenkins configurations.
We recommend that the Jenkins configuration is stored in a folder called `.jenkins` at the root of your repository.
1. Create `.jenkins/docker/Dockerfile`

    see example of this file in [docker/Dockerfile](./docker/Dockerfile)
1. Add your project's job configuration. For example, if your project/repository is called `hello-world`, add `.jenkins/docker/contrib/jenkins/configuration/jobs/hello-world/config.xml`
    seet example of this file in docker/contrib/jenkins/configuration/jobs/hello-world/config.xml
    Make sure to update the following.
    1. `<id>08659502-ae8e-4300-a3b4-be5ec7fb9bd7</id>` by generating a random (uuid)[https://www.uuidgenerator.net/]
    2. `<repoOwner>bcgov</repoOwner>` and `<repository>hello-world</repository>`
    3. `<scriptPath>Jenkinsfile</scriptPath>`
    
    
