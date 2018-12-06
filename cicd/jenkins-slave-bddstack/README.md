# Troubleshooting
For troubleshooting errors when running test scripts, the best way is to run the image and startup chrome.

From one terminal, startup a container with chrome:
```
#make sure you are in the correct namespace/project (e.g.:bcgov-tools)
oc project bcgov-tools

#example 1
oc run bdd --image=docker-registry.default.svc:5000/bcgov/jenkins-slave-bddstack:v1-latest -it --rm=true --restart=Never --image-pull-policy=Always --command -- google-chrome --headless --disable-gpu --no-sandbox --disable-setuid-sandbox --disable-software-rasterizer --remote-debugging-port=9222 http://dev-test.nemikor.com/web-storage/support-test/

#example 2
oc run bdd --image=docker-registry.default.svc:5000/bcgov/jenkins-slave-bddstack:v1-latest -it --rm=true --restart=Never --image-pull-policy=Always --command -- google-chrome --headless --disable-gpu --no-sandbox --disable-setuid-sandbox --disable-software-rasterizer --remote-debugging-port=9222  https://codepen.io/gab/full/AxFoB/

```

From another terminal, start the port forward:
```
#make sure you are in the correct namespace/project:
oc port-forward bdd 9222
```

From a a local chrome browser, navigate to `http://localhost:9222/`

