from cubicweb.__pkginfo__ import numversion as cw_version

# flake8: noqa: F401
if cw_version < (4, 0):
    from cubicweb.pyramid.test import ACCEPTED_ORIGINS
