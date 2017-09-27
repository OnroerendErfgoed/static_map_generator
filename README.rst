Static Map Generator
====================

The goal of this Static Map Generator (SMG) is to generate static maps
that are composed of:

-   different geographical formats like GeoJSON
-   a background layer like WMS
-   layout-overlays like Text, and Scale.

Based on a configuration file, the SMG renders all individual layers to
a temporary image.

The image will contain a scale bar.

The image can be returned as a steam or a base64 format.