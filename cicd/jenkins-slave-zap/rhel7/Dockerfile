FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7

EXPOSE 8080

ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
   
ENV SUMMARY="OWASP ZAP Jenkins slave." \
    DESCRIPTION="Jenkins pipeline slave with OWASP ZAP."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Jenkins-Pipeline-OWASP-ZAP" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jenkins-jnlp-owasp-zap,jenkins-jnlp" \
      release="1"
      
# NOTES:
# We need to call 2 (!) yum commands before being able to enable repositories properly
# This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1479388
# Chrome install info: https://access.redhat.com/discussions/917293
RUN yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-fastrack-rpms && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum clean all -y && \
    yum update -y

RUN yum install -y redhat-rpm-config \
    make automake autoconf gcc gcc-c++ \
    libstdc++ libstdc++-devel \
    wget curl git firefox \
    xmlstarlet gettext tar \
    x11vnc xorg-x11-server-Xvfb xterm \
    openbox net-tools nss_wrapper \
    python python-pip \
    java-11-openjdk-headless java-11-openjdk java-11-openjdk-devel && \
    yum clean all

RUN pip install --upgrade pip
RUN pip install zapcli
RUN pip install python-owasp-zap-v2.4

RUN if [ ! -d /tmp/.X11-unix ] ; then mkdir /tmp/.X11-unix; fi && \
    mkdir -p /zap/wrk && \
    mkdir /zap@tmp && \
    mkdir -p /var/lib/jenkins/.vnc

ADD zap /zap/

# Copy the entrypoint
COPY configuration/* /var/lib/jenkins/

ENV PATH /zap:$PATH
ENV ZAP_PATH /zap/zap.sh
ENV HOME /var/lib/jenkins

# Default port for use with zapcli
ENV ZAP_PORT=8080

COPY policies /var/lib/jenkins/.ZAP/policies/
COPY .xinitrc /var/lib/jenkins/

WORKDIR /zap

ENV WEBSWING_VERSION=2.7.1

# Download and expand the latest stable release 
RUN curl -s https://raw.githubusercontent.com/zaproxy/zap-admin/master/ZapVersions-dev.xml | xmlstarlet sel -t -v //url |grep -i Linux | wget -q --content-disposition -i - -O - | tar zx --strip-components=1 && \
    curl -s -L https://bitbucket.org/meszarv/webswing/downloads/webswing-${WEBSWING_VERSION}.zip | jar -x && \
    touch AcceptedLicense
    
ADD webswing.config /zap/webswing-${WEBSWING_VERSION}/webswing.config

RUN chown -v -R root:root /zap && \
    chown -v -R root:root /var/lib/jenkins && \
    chmod -v -R 777 /var/lib/jenkins && \
    chmod -v -R 777 /zap && \
    chmod -v -R 777 /zap@tmp && \
    chmod -v -R 1777 /tmp/.X11-unix && \
    chown -v -R root:root /tmp/.X11-unix/

WORKDIR /var/lib/jenkins

ENV OPENSHIFT_JENKINS_JVM_ARCH=x86_64

USER 1001
