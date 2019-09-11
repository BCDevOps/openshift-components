FROM registry.access.redhat.com/ubi7/ubi-minimal

ARG ARTIFACTORY_URL=https://bwa.nrs.gov.bc.ca/int/artifactory
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS
ARG OC_NAME=openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit

# libnsl is required for rhel8
RUN microdnf --nodocs install tar unzip libaio java-1.8.0-openjdk ncurses && \
    curl -sSL -o /tmp/${OC_NAME}.tar.gz https://github.com/openshift/origin/releases/download/v3.11.0/${OC_NAME}.tar.gz && \
    tar -xzf /tmp/${OC_NAME}.tar.gz -C /usr/local/bin/ --strip=1 ${OC_NAME}/oc && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/instant-client/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm" && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/instant-client/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm" && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/sqlcl-19.2.1.206.1649.zip "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/sqlcl/sqlcl-19.2.1.206.1649.zip" && \
    rpm -i /tmp/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm && \
    rpm -i /tmp/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm && \
    unzip -nq /tmp/sqlcl-19.2.1.206.1649.zip -d /opt/ && \
    ln -s /opt/sqlcl/bin/sql /usr/local/bin/sqlcl && \
    rm -rf /tmp/* && \
    microdnf clean all
WORKDIR /opt/src
