FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7

EXPOSE 8080

ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
    
ENV SUMMARY="Jenkins slave with chrome and firefox installed for use with functional/BDD tests that use BDDStack." \
    DESCRIPTION="Jenkins pipeline slave with chrome and firefox for testing application with headless browser. (aka 'BDDStack')"

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Jenkins-Pipeline-BDDStack" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jenkins-jnlp-chrome,jenkins-jnlp-firefox,jenkins-jnlp" \
      release="1"
      
COPY contrib/bin/scl_enable /usr/local/bin/scl_enable

# NOTES:
# We need to call 2 (!) yum commands before being able to enable repositories properly
# This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1479388
# Chrome install info: https://access.redhat.com/discussions/917293
RUN yum repolist > /dev/null && \
    yum install -y yum-utils && \
    yum-config-manager --disable \* &> /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-fastrack-rpms && \
    UNINSTALL_PKGS="java-1.8.0-openjdk-headless.i686" &&\
    INSTALL_PKGS="redhat-lsb libXScrnSaver gdk-pixbuf2 xorg-x11-server-Xvfb wget firefox rh-nodejs6 rh-nodejs6-npm rh-nodejs6-nodejs-nodemon nss_wrapper" && \
    yum remove -y $UNINSTALL_PKGS &&\
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all -y && \
    ln -s /usr/lib/node_modules/nodemon/bin/nodemon.js /usr/bin/nodemon && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum -y localinstall google-chrome-stable_current_x86_64.rpm && \
    rm google-chrome-stable_current_x86_64.rpm && \
    if [ ! -d /home/jenkins/.pki ] ; then mkdir /home/jenkins/.pki; fi && \
    chmod -R 777 /home/jenkins/.pki

# . /opt/rh/rh-nodejs6/enable
ENV PATH=/opt/rh/rh-nodejs6/root/usr/bin${PATH:+:${PATH}} \
    LD_LIBRARY_PATH=/opt/rh/rh-nodejs6/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} \
    PYTHONPATH=/opt/rh/rh-nodejs6/root/usr/lib/python2.7/site-packages${PYTHONPATH:+:${PYTHONPATH}} \
    MANPATH=/opt/rh/rh-nodejs6/root/usr/share/man:$MANPATH
    
# Update `npm` past what is supplied in `rh-nodejs6` to a more mondern
# version that supports the `ci` option. This will greatly speed up
# package installs in a ci environment. It also cleans the package
# cache.
RUN source scl_source enable rh-nodejs6 && \
    npm i -g yarn@latest && \
    npm i -g nsp@latest && \
    rm -rf ~/.npm
    
ENV OPENSHIFT_JENKINS_JVM_ARCH=x86_64

USER 1001
