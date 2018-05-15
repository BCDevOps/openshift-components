# OpenShift Oracle InstantClient #

This repository can be used for chained builds that require Oracle Instant Client software RPM's.
The docker image is a base rhl7 image containing the oracle rpms.
The cahined build siply copies the oracle rpms from this image and installs it. 
This way we don't store oracle rpms on github. 


## Source ##

These RPM's were obtained from the [Oracle Technology Network] (http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html):
 - oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
 - oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
 - oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm

Refer to the above URL for a reference to the subsequent steps necessary to install the RPM's on RHEL.

Chained builds can reference the files at:
```
/tmp/oraclelibs/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
/tmp/oraclelibs/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
/tmp/oraclelibs/oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm
```

## License

Code released under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

