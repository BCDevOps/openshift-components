FROM registry.access.redhat.com/ubi7/ubi-minimal

ARG ARTIFACTORY_URL=https://bwa.nrs.gov.bc.ca/int/artifactory
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS
ARG OC_VERSION=3.11.0
ARG OC_NAME=openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit
ARG LIQUIBASE_VERSION=3.8.0
ARG ORACLE_CLIENT_VERSION=19.3.0.0.0-1
ARG ORACLE_SQLCL_VERSION=19.2.1.206.1649

# libnsl is required for rhel8
RUN microdnf --nodocs install tar unzip libaio java-1.8.0-openjdk ncurses openssl && \
    echo "Installing OC ${OC_VERSION}" && \
    curl -sSL -o /tmp/${OC_NAME}.tar.gz https://github.com/openshift/origin/releases/download/v${OC_VERSION}/${OC_NAME}.tar.gz && \
    tar -xzf /tmp/${OC_NAME}.tar.gz -C /usr/local/bin/ --strip=1 ${OC_NAME}/oc && \
    echo "Installing Oracle Instant Client (basic) ${ORACLE_CLIENT_VERSION}" && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/instant-client/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm" && \
    rpm -i /tmp/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm && \
    echo "Installing Oracle Instant Client (sqlplus) ${ORACLE_CLIENT_VERSION}" && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/instant-client/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm" && \
    rpm -i /tmp/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm && \
    echo "Installing Oracle SQLCl ${ORACLE_SQLCL_VERSION}" && \
    curl -sSL -u "${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}" -o /tmp/sqlcl-${ORACLE_SQLCL_VERSION}.zip "${ARTIFACTORY_URL}/ext-binaries-local/com/oracle/sqlcl/sqlcl-${ORACLE_SQLCL_VERSION}.zip" && \
    unzip -nq /tmp/sqlcl-${ORACLE_SQLCL_VERSION}.zip -d /opt/ && \
    ln -s /opt/sqlcl/bin/sql /usr/local/bin/sqlcl && \
    echo "Installing Liquibase ${LIQUIBASE_VERSION}" && \
    mkdir -p /opt/liquibase/${LIQUIBASE_VERSION} && \
    curl -sSL -o /tmp/liquibase-${LIQUIBASE_VERSION}-bin.tar.gz https://github.com/liquibase/liquibase/releases/download/liquibase-parent-${LIQUIBASE_VERSION}/liquibase-${LIQUIBASE_VERSION}-bin.tar.gz && \
    tar -xzf /tmp/liquibase-${LIQUIBASE_VERSION}-bin.tar.gz -C /opt/liquibase/${LIQUIBASE_VERSION} 'liquibase' 'liquibase.jar' 'lib/*' && \
    ln -s /opt/liquibase/${LIQUIBASE_VERSION}/liquibase /usr/local/bin/liquibase && \
    rm -rf /tmp/* && \
    microdnf clean all
WORKDIR /opt/src
