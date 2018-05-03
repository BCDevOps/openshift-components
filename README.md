[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# OpenShift Components

Useful components for day to day operations on OpenShift. 

## apps

Templates for build / deployment and useful support applications    

## cicd

Docker files to build Jenkins builder images

__Android__

This image contains OpenJSK >= 1.8.0 and the Android
SDK manager / tools for `gradle` builds. See the
Docker file for more precise version information.

__BDD Stack__

__Python3__

This image contains Python 3 and support tools like
`pip`.

__Python 3 & node.js 6.11__

This image contains Python 3 (with `pip`) and RedHat node.js 6.11 (with `npm`).

__node.js 6.11__

This image contains __stock__ node.js 6.11 with the
latest `npm` (>= 6.0.0), `yarn`, and `nsp` cli tools installed
globally; see NODE_HOME to find installed components.

npm > 5.7.0 has the `ci` option that greatly increases
package install in a ci environment. Consider using it!

__Sonar__

__Zap__

## db

Docker files to build data storage images

- **PostGIS** RHEL7 PostgreSQL 9.6 base image with PostGIS 2.4 extension(s). 
