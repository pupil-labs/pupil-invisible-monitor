"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2019 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""

from contextlib import contextmanager

import OpenGL
from OpenGL.GL import *

# OpenGL.FULL_LOGGING = True
OpenGL.ERROR_LOGGING = False


def basic_gl_setup():
    glEnable(GL_POINT_SPRITE)
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)  # overwrite pointsize
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_LINE_SMOOTH)


@contextmanager
def use_viewport(x, y, width, height):
    width = max(0, width)
    height = max(0, height)

    glPushAttrib(GL_VIEWPORT_BIT)
    glViewport(x, y, width, height)

    yield

    glPopAttrib()


@contextmanager
def use_coordinate_system(left, right, bottom, top):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1, 1)  # gl coord convention

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    yield

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def use_norm_based_coordinate_system():
    # more descriptive shortcut for common coordinates
    return use_coordinate_system(0, 1, 0, 1)
