# This dockerfile builds the zap stable release
FROM centos:centos7
MAINTAINER Deven Phillips <deven.phillips@redhat.com>

RUN yum install -y epel-release && \
    yum clean all
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


# upgrade pip and install the latest dev version of the python API
RUN pip install --upgrade pip
RUN pip install zapcli
RUN pip install python-owasp-zap-v2.4

RUN mkdir -p /zap/wrk
ADD zap /zap/

RUN mkdir -p /var/lib/jenkins/.vnc

# Copy the entrypoint
COPY configuration/* /var/lib/jenkins/
COPY configuration/run-jnlp-client /usr/local/bin/run-jnlp-client

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:/zap:$PATH
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

RUN chown -R root:root /zap && \
    chown -R root:root /var/lib/jenkins && \
    chmod -R 777 /var/lib/jenkins && \
    chmod -R 777 /zap && \
    chmod 777 /
    

WORKDIR /var/lib/jenkins

# Run the Jenkins JNLP client
ENTRYPOINT ["/usr/local/bin/run-jnlp-client"]
