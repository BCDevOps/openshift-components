FROM registry.access.redhat.com/ubi8/ubi-minimal

ARG SECRET

RUN microdnf --nodocs install tar libaio libnsl java-1.8.0-openjdk ncurses && \
#    rpm -i /tmp/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm && \
#    rpm -i /tmp/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm && \
#    unzip -nq /tmp/sqlcl-19.2.1.206.1649.zip -d /opt/ && \
     echo "found secret '${SECRET}'" && \
     microdnf clean all
WORKDIR /opt/src
