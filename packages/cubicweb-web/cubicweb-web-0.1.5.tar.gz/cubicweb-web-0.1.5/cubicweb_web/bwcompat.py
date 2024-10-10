from cubicweb.__pkginfo__ import numversion as cw_version

# flake8: noqa: F401
if cw_version < (4, 0):
    from cubicweb.pyramid.core import CubicWebPyramidRequest
    from cubicweb.pyramid.bwcompat import (
        CubicWebPyramidHandler,
        PyramidSessionHandler,
    )
