FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7

# Note this is based mostly on https://github.com/sclorg/s2i-python-container/blob/master/3.5/Dockerfile.rhel7

EXPOSE 8080

ENV SUMMARY="Jenkins slave with python 3 and nodejs 6" \
    DESCRIPTION="Jenkins pipeline slave with python 3 and nodejs 6 installed" \
    PYTHON_VERSION=3.5 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    BASH_ENV=/usr/local/bin/scl_enable \
    ENV=/usr/local/bin/scl_enable \
    PROMPT_COMMAND=". /usr/local/bin/scl_enable" \
    PATH=/opt/rh/rh-nodejs6/root/usr/bin${PATH:+:${PATH}} \
    LD_LIBRARY_PATH=/opt/rh/rh-nodejs6/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} \
    PYTHONPATH=/opt/rh/rh-nodejs6/root/usr/lib/python2.7/site-packages${PYTHONPATH:+:${PYTHONPATH}} \
    MANPATH=/opt/rh/rh-nodejs6/root/usr/share/man:$MANPATH \
    OPENSHIFT_JENKINS_JVM_ARCH=x86_64 \
    PATH=/zap:$PATH \
    ZAP_PATH=/zap/zap.sh \
    ZAP_PORT=8080

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Jenkins-Pipeline-python-nodejs" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jenkins-jnlp-python,jenkins-jnlp-nodejs,jenkins-jnlp" \
      release="1"

COPY contrib/bin/scl_enable /usr/local/bin/scl_enable

# We need to call 2 (!) yum commands before being able to enable repositories properly
# This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1479388
#
# Update `npm` past what is supplied in `rh-nodejs6` to a more mondern
# version that supports the `ci` option. This will greatly speed up
# package installs in a ci environment. Also, install the `yarn` package
# manager and node security project (`nsp`) CLI tool.
#
# In order to drop the root user, we have to make some directories world
# writable as OpenShift default security model is to run the container under
# random UID.

RUN yum repolist > /dev/null && \
    yum install -y yum-utils && \
    yum-config-manager --disable \* &> /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    INSTALL_PKGS="rh-python35 rh-python35-python-devel rh-python35-python-setuptools rh-python35-python-pip \
	nss_wrapper httpd24 httpd24-httpd-devel httpd24-mod_ssl httpd24-mod_auth_kerb httpd24-mod_ldap httpd24-mod_session \
        atlas-devel gcc-gfortran libffi-devel libtool-ltdl rh-nodejs6 rh-nodejs6-nodejs-nodemon" && \
    ln -s /usr/lib/node_modules/nodemon/bin/nodemon.js /usr/bin/nodemon && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    # Remove redhat-logos (httpd dependency) to keep image size smaller.
    rpm -e --nodeps redhat-logos && \
    yum clean all -y && \
    source scl_source enable rh-nodejs6 && \
    npm i -g yarn@latest && \
    npm i -g nsp@latest && \
    rm -rf ~/.npm && \
    mkdir -p /opt/app-root  && \
    chown -R 1001:0 /opt/app-root && \
    chmod -R og+rwx /opt/app-root && \ 
    yum install -y redhat-rpm-config \
    make automake autoconf gcc gcc-c++ libstdc++ libstdc++-devel \
    java-1.8.0-openjdk.x86_64 java-1.8.0-openjdk-headless.x86_64 java-1.8.0-openjdk-devel.x86_64 \
    wget nano curl git gzip gettext tar xorg-x11-server-Xvfb xterm vnc-server \
    net-tools python27-python-pip firefox nss_wrapper  && \
    yum -y clean all

RUN wget https://pypi.python.org/packages/source/s/setuptools/setuptools-7.0.tar.gz --no-check-certificate && \
    tar xzf setuptools-7.0.tar.gz && \
    cd setuptools-7.0 && \
    python setup.py install && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    pip install --upgrade pip && \
    pip install zapcli && \
    pip install python-owasp-zap-v2.4

COPY contrib/zap/rpms/*.rpm ./
RUN yum -y localinstall xmlstarlet-1.6.1-1.el7.x86_64.rpm && \
    yum -y localinstall imlib2-1.4.5-9.el7.x86_64.rpm && \
    yum -y localinstall pyxdg-0.25-2.el7.nux.noarch.rpm && \
    yum -y localinstall openbox-libs-3.5.2-6.2.x86_64.rpm && \
    yum -y localinstall openbox-3.5.2-6.2.x86_64.rpm && \
    yum -y localinstall x11vnc-0.9.13-11.el7.x86_64.rpm && \
    yum -y clean all && \
    rm ./*.rpm && \
    if [ ! -d /tmp/.X11-unix ] ; then mkdir /tmp/.X11-unix; fi && \
    mkdir -p /zap/wrk && \
    mkdir /zap@tmp && \
    mkdir -p /var/lib/jenkins/.vnc

ADD contrib/zap/zap /zap/
COPY contrib/zap/configuration/* /var/lib/jenkins/
COPY contrib/zap/policies /var/lib/jenkins/.ZAP/policies/
COPY contrib/zap/.xinitrc /var/lib/jenkins/
ADD contrib/zap/webswing.config /zap/webswing-2.3/webswing.config

WORKDIR /zap
# Download and expand the latest stable release 
RUN curl -s https://raw.githubusercontent.com/zaproxy/zap-admin/master/ZapVersions-dev.xml | xmlstarlet sel -t -v //url |grep -i Linux | wget -q --content-disposition -i - -O - | tar zx --strip-components=1 && \
    curl -s -L https://bitbucket.org/meszarv/webswing/downloads/webswing-2.3-distribution.zip | jar -x && \
    touch AcceptedLicense && \
    chown -v -R root:root /zap && \
    chown -v -R root:root /var/lib/jenkins && \
    chmod -v -R 777 /var/lib/jenkins && \
    chmod -v -R 777 /zap && \
    chmod -v -R 777 /zap@tmp && \
    chmod -v -R 1777 /tmp/.X11-unix && \
    chown -v -R root:root /tmp/.X11-unix/

WORKDIR /var/lib/jenkins

USER 1001
