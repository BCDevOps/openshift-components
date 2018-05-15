FROM rhel7

RUN mkdir /tmp/oraclelibs/

COPY /tmp/oraclelibs/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm /tmp/oraclelibs/
COPY /tmp/oraclelibs/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm /tmp/oraclelibs/
Copy /tmp/oraclelibs/oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm /tmp/oraclelibs

RUN chmod -R 755 /tmp/oraclelibs/

USER 10001
