**********************************
Johannesmann Spatial Tessellation
**********************************

Python implementation of the Johannesmann Spatial Tessellation method.

This method was developed for the occasion of Sarah Johannesmann's doctoral
thesis defence and is inspired by the way she cuts a cake. For a
two-dimensional, bounded plane this is realised by subdividing the plane by a
line, which intersects a random point on the plane at a random slope, resulting
in two tiles. The process is repeated an arbitrary number of times, with each
new line subdividing only the tile the random origin point is located.


Features
========

* Implementation of two-dimensions.
* Single point and grid sampling methods.


Example
=======

Import the package by::

    import johannesmann

Create a tessellation object with size 4 by 4 with 30 cuts::

    tsl = johannesmann.Tessellation(4, 4, 30)

Sample the tile ID number at the centre of the tessellated plane::

    center_id = tsl.tile_id(0, 0)

Sample the whole bounded plane (from -2 to 2 in both dimension) with a grid of
1000 by 1000 samples to get an image of the tessellation. Set `squash_ids=True`
to decrease the range of tile ID numbers by renumbering and removing unused
ID numbers::

    image = tsl.tile_id_grid(1000, 1000, squash_ids=True)
