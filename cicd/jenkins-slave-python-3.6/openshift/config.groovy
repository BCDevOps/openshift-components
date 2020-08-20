app {
    name = "${opt.'name'?:'jenkins-slave-python-3.6'}"
    namespaces { //can't call environments :(
        'build'{
            namespace = 'bcgov-tools'
            disposable = true
        }
        'dev' {
            namespace = 'bcgov'
            disposable = true
        }
        'prod' {
            namespace = 'bcgov'
            disposable = false
        }
    }

    git {
        workDir = ['git', 'rev-parse', '--show-toplevel'].execute().text.trim()
        uri = ['git', 'config', '--get', 'remote.origin.url'].execute().text.trim()
        ref = "refs/pull/${opt.'pr'}/head"
        commit = ['git', 'rev-parse', 'HEAD'].execute().text.trim()
    }

    build {
        env {
            name = "build"
            id = "pr-${opt.'pr'}"
        }
        suffix = "-build-${opt.'pr'}"
        id = "${app.name}${app.build.suffix}"
        version = "${app.build.env.name}-v${opt.'pr'}"
        name = "${opt.'build-name'?:app.name}"

        namespace = app.namespaces.'build'.namespace
        timeoutInSeconds = 60*20 // 20 minutes
        templates = [
                [
                    'file':'cicd/jenkins-slave-python-3.6/openshift/build.yaml',
                    'params':[
                        'NAME': app.build.name,
                        'SUFFIX': app.build.suffix,
                        'VERSION': app.build.version,
                        'SOURCE_REPOSITORY_URL': "${app.git.uri}",
                        'SOURCE_REPOSITORY_REF': "${app.git.ref}"
                    ]
                ]
        ]
    }
}
