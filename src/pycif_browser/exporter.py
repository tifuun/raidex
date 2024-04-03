"""
"""

from io import IOBase, StringIO
import typing
from pathlib import Path
from dataclasses import dataclass
from itertools import groupby

import numpy as np

import pycif as pc

def _export_layer(stream, geoms, bbox, norm_height=90):

    scale_factor = norm_height / bbox.height

    bbox = bbox.copy()
    bbox.max_x *= scale_factor
    bbox.max_y *= scale_factor
    bbox.min_x *= scale_factor
    bbox.min_y *= scale_factor
    # TODO define arithmetic operations on bbox?

    stream.write(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        #f'width="{bbox.width}" '
        #f'height="{bbox.height}" '
        'class="layer-image" '
        f'viewBox="{bbox.left} 0 {bbox.width} {bbox.height}"'
        '>\n'
        )

    stream.write(
        '<defs>\n'

        '<pattern '
        'id="hatch" '
        'patternUnits="userSpaceOnUse" width="4" height="4">'
        '<path d="M-1,1 l2,-2'
        '   M0,4 l4,-4'
        '   M3,5 l2,-2" '
        '   style="stroke:#FFFFFF; stroke-width:1" />'
        #'   style="stroke:currentColor; stroke-width:1" />'
        '</pattern>\n'

        '<mask id="hatch-mask" x="0" y="0" width="1" height="1" >\n'
        '<rect x="-100" y="0" width="200" height="100" fill="url(#hatch)" />\n'
        '</mask>\n'

        '</defs>\n'
        )

    # THANK YOU
    # https://stackoverflow.com/questions/43423317/how-to-change-color-of-svg-pattern-on-usage/53158433#53158433
    # Using mask allows us to dynamically recolor the hatching pattern


    for geom in geoms:

        stream.write(
            '<polygon '
            'mask="url(#hatch-mask)" '
            #'fill="url(#hatch)" '
            'fill="currentColor" '
            #'stroke="#FF0000" '
            #'stroke="currentColor" '
            #'stroke-width="1" '
            'points="'
            )

        try:
            for point in geom:
                x = point[0] * scale_factor
                y = bbox.top - point[1] * scale_factor
                stream.write(f'{x},{y} ')

        except Exception as e:
            raise Exception(
                f'Failed to export geom {geom}. ',
                ) from e

        stream.write('" />\n')

        # TODO very messy copy-pasted code here.
        # I think it would be best to use jinja2
        # to generate the SVGs as well!

        stream.write(
            '<polygon '
            'fill="none" '
            #'stroke="#FF0000" '
            'stroke="currentColor" '
            'stroke-width="1" '
            'points="'
            )

        try:
            for point in geom:
                x = point[0] * scale_factor
                y = bbox.top - point[1] * scale_factor
                stream.write(f'{x},{y} ')

        except Exception as e:
            raise Exception(
                f'Failed to export geom {geom}. ',
                ) from e

        stream.write('" />\n')

    stream.write('</svg>\n')

def _group(compo: pc.Compo):
    #keyfunc = lambda subpoly: subpoly.layer
    #subpolys = sorted(
    #    compo.get_subpolygons(),
    #    key=keyfunc
    #    )
    #grouped = groupby(subpolys, keyfunc)

    #return grouped

    #grouped = {layer: [] for layer in compo.Layers.keys()}
    grouped = {}
    for layer_name, layer in compo.get_geoms().items():
        if layer_name not in grouped.keys():
            grouped[layer_name] = []
        for geom in layer:
            grouped[layer_name].append(geom)

    return grouped 

#def export_compo_as_files(
#        compo: pc.compo,
#        dest: Path,
#        ):
#
#    bbox = compo.bbox.pad(10)
#    grouped = _group(compo)
#
#    paths = []
#    for layer_name, layer_subpolys in enumerate(grouped):
#        svgpath = dest / f'layer_{i}.svg'
#        with svgpath.open('w') as file:
#            _export_layer(file, layer_subpolys, bbox)
#        paths.append(svgpath)
#
#    return paths
#
#    # TODO layer order!

def export_compo_as_inline(
        compo: pc.Compo,
        ):

    bbox = compo.bbox.pad(10)
    grouped = _group(compo)

    images = []
    for layer_name, layer_subpolys in grouped.items():
        stream = StringIO()
        _export_layer(stream, layer_subpolys, bbox)
        images.append(stream.getvalue())
    return images

    # TODO layer order!
