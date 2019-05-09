---

description: A PostgreSQL Docker image that includes PostGIS and dependencies needed to support GDAL.
title: PostGIS
image: https://commons.wikimedia.org/wiki/File:Logo_square_postgis.png
---

## PostGIS
> PostgreSQL 9.6 with PostGIS 2.4 Extension

### Summary

This image extends the RHEL7 base PostgreSQL 9.6 image by adding PostGIS 2.4 from postgresql.org and dependencies from fedoraproeject.org needed to support GDAL.

### Setup and Install

When you deploy this image the database will not have the PostGIS extension(s) created by default. To enable them use the following two SQL commands:

```console
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

You can verify the install with the following SQL command:

```console
SELECT postgis_full_version();
POSTGIS="2.4.3 r16312" PGSQL="96" GEOS="3.6.2-CAPI-1.10.2 4d2925d6"
PROJ="Rel. 4.9.3, 15 August 2016" GDAL="GDAL 1.11.4, released 2016/01/25"
LIBXML="2.9.1" LIBJSON="0.11" TOPOLOGY RASTER
```

 This image does *not* include the [PoostGIS Foreign Data Wrapper(s)]( https://wiki.postgresql.org/wiki/Foreign_data_wrappers) so the command to create this extension will not work:

 ```console
 postgres=# CREATE EXTENSION ogr_fdw;
 ERROR:  could not open extension control file "/opt/rh/rh-postgresql96/root/usr/share/pgsql/
 extension/ogr_fdw.control": No such file or directory
 ```
 ### Closing

A running docker container will have these supper usefull command line tools; they can be used for loading in `raster` and `shape` files: 

* pgsql2shp 
* raster2pgsql
* shp2pgsql

## Contributing

Lets make the world a better place one pull request at a time. Fork fork the project and create a PR. We'll see it and work with you.

 
