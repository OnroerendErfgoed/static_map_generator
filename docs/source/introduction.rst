============
Introduction
============

The goal of this Static Map Generator (SMG) is to generate static maps that are composed of:

* different geographical formats: WMS, WKT, GeoJSON, ...
* Layout-overlays: Text, Logo, Scale, ...

Based on a configuration file, the SMG renders all individual layers to temporary images and combines these temporary images to the final output image.

Use
=======

As a Library
------------
* Import Generator from static_map_generator.generator
* Create a configuration file
* Generator.generate('config')

As a Service
------------
* POST the config-file (json) to the REST endpoint: http://localhost:6543/maps
* The service returns the generated image

Example
=======

Let's clarify this with an example:

Library
-------

.. literalinclude:: /../../examples/map_simple.py
    :language: python


Service
-------



Configuration
==============

The configuration is a json-object existing out of 2 basic keys:

============    ========================================    ==========  ==========
Key             Description                                 Type        Mandatory
============    ========================================    ==========  ==========
'params'        general parameters for the final map        Object      True
'layers'        an array of 'layer' for the final map       Array       True
============    ========================================    ==========  ==========

params-object
-------------

============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'filename'      path for the output map                             String      True        'simple.png'
'epsg'          spatial reference system - epsg                     Integer     True        4326
'filetype'      Format for the output map                           String      True        'png'
'width'         width for the output map                            Integer     True        500
'height'        height for the output map                           Integer     True        500
'bbox'          an array of coordinates to define bounding box      Array       True        [4, 50, 5, 51]
============    ================================================    ==========  ==========  ===============

layer-object
-------------
The parameters for each layer differ based on the type of layer:

WMS
^^^^^^^

============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'type'          Type of layer                                       String      True        'wms'
'url'           url of the wms-service                              String      True        'https://geo.onroerenderfgoed.be/geoserver/wms?'
'layers'        layernames to be used in wms-service                String      True        'vioe_geoportaal:landschapsbeheersplannen'
============    ================================================    ==========  ==========  ===============

Notice: Next to these parameters, other supported parameters of the wms-service can be given, f.e featureid, bgcolor, transparant, ...


GeoJSON
^^^^^^^
============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'type'          Type of layer                                       String      True        'geojson'
'geojson'       geojson-notation of geometry                        String      True        {'crs': {'type': 'name', 'properties': {'name': 'EPSG:31370'}}, 'type': 'MultiPoint', 'coordinates': [[103912.03, 192390.11],[103500, 192390.11]]}
'color'         colorcode (RGB, HEX, named color)                   String      True        'steelblue'
'opacity'       opacity                                             Numeric     True        0.6
============    ================================================    ==========  ==========  ===============

WKT
^^^^^^^

============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'type'          Type of layer                                       String      True        'wkt'
'wkt'           WKT-notation of geometry                            String      True        'POLYGON ((4.5 50.2, 5 50.2, 5 50, 4.5 50.2))'
'color'         colorcode (RGB, HEX, named color)                   String      True        'steelblue'
'opacity'       opacity                                             Numeric     True        0.6
============    ================================================    ==========  ==========  ===============


Logo
^^^^^^

============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'type'          Type of layer                                       String      True        'logo'
'path'          path of the logo to be used                         String      True        'logo.png'
'url'           url of the logo to be used                          String      True        'https://www.onroerenderfgoed.be/assets/img/logo-og.png'
'opacity'       opacity                                             Numeric     True        0.6
============    ================================================    ==========  ==========  ===============

Text
^^^^^^

============    ================================================    ==========  ==========  ===============
Key             Description                                         Type        Mandatory   Example
============    ================================================    ==========  ==========  ===============
'type'          Type of layer                                       String      True        'text'
'text'          Text to be used for the layer                       String      True        'This is a test'
'font_size'     Font size                                           Integer     True        24
'text_color'    colorcode (RGB, HEX, named color)                   String      True        'steelblue'
============    ================================================    ==========  ==========  ===============

Scale
^^^^^^^

Not implemented yet

Legend
^^^^^^^

Not implemented yet



Development
===========
First of all, Mapnik (2.3) and all dependencies has to be installed on your machine. Please use the following instructions:
https://github.com/mapnik/mapnik/wiki/UbuntuInstallation

.. code-block:: bash
    $ pip install -r requirements-dev.txt
    $ pserve development.ini

We try to cover as much code as we can with unit tests. You can run them using
tox_ or directly through pytest. When providing a pull request, please run the
unit tests first and make sure they all pass. Please provide new unit tests
to maintain 100% coverage.

.. code-block:: bash

    $ tox
    # No coverage
    $ py.test
    # Coverage
    $ py.test --cov static_map_generator --cov-report term-missing
    # Only run a subset of the tests
    $ py.test static_map_generator/tests/test_renderer.py

.. _tox: http://tox.testrun.org
