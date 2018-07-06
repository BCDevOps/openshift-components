FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7

ARG NODE_MAJOR_VERSION=8
ARG NODE_VERSION=node-v8.11.3
ARG NODE_LOCATION=v8.11.3

ENV SUMMARY="Jenkins slave with stock nodejs ${NODE_VERSION}"  \
    DESCRIPTION="Jenkins pipeline slave with stock nodejs ${NODE_VERSION}"

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="jenkins-pipeline-nodejs${NODE_MAJOR_VERSION}" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jenkins-jnlp-nodejs,jenkins-jnlp-nodejs${NODE_MAJOR_VERSION},jenkins-jnlp" \
      release="1"

ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 

# We need to call 2 (!) yum commands before being able to enable repositories properly
# This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1479388
RUN yum repolist > /dev/null && \
    yum install -y yum-utils && \
    yum-config-manager --disable \* &> /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    INSTALL_PKGS="nss_wrapper httpd24 httpd24-httpd-devel httpd24-mod_ssl httpd24-mod_auth_kerb \
        httpd24-mod_ldap httpd24-mod_session atlas-devel gcc-gfortran libffi-devel libtool-ltdl" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    # Remove redhat-logos (httpd dependency) to keep image size smaller.
    rpm -e --nodeps redhat-logos && \
    yum clean all -y && \
    rm -rf /var/cache/yum

# Fetch stock nodejs and install
RUN mkdir -p /opt && \
    pushd /opt && \
    curl -s https://nodejs.org/dist/${NODE_LOCATION}/${NODE_VERSION}-linux-x64.tar.xz | tar -Jx && \
    rm -f ${NODE_VERSION}-linux-x64.tar.xz

# Update environment variables
ENV NODE_HOME=/opt/${NODE_VERSION}-linux-x64 \
    PATH=$PATH:/opt/${NODE_VERSION}-linux-x64/bin

# Update the version of `npm` that came with the packages above
# and install a few additional tools.
RUN npm i -g npm@latest yarn@latest nsp@latest nodemon@latest && \
    rm -rf ~/.npm && \
    node -v && \
    npm -v

EXPOSE 8080

USER 1001
