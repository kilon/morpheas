"""
Some necessary functions for Morpheas to work correctly.
"""

import math
import bpy
import bgl
import blf
import bpy_extras


def drawRegion(mode, points, color):
    """
    Draw a simple shape with given points and color.
    """

    bgl.glColor4f(color[0], color[1], color[2], color[3])
    if mode == 'GL_LINE_LOOP':
        bgl.glBegin(bgl.GL_LINE_LOOP)
    else:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_POLYGON)

    # start with corner right-bottom
    for point in points:
        bgl.glVertex2f(point[0], point[1])

    bgl.glEnd()


def drawArc(cx, cy, r, startAngle, arcAngle, numSegments):
    """
    Draw an arc.
    (cx, cy) is the center of circle, r is strength value,
    startAngle and arcAngle in radians, numSegments is the number of points
    that make the arc.
    """
    theta = arcAngle / float(numSegments - 1)
    tangetialFactor = math.tan(theta)
    radialFactor = math.cos(theta)

    x = r * math.cos(startAngle)
    y = r * math.sin(startAngle)
    verts = []
    for i in range(numSegments):
        verts.append((x + cx, y + cy))

        tx = -y
        ty = x

        x += tx * tangetialFactor
        y += ty * tangetialFactor

        x *= radialFactor
        y *= radialFactor
    return verts


def roundCorners(x1, y1, x2, y2, value, steps, corners=[True, True, True, True]):
    """
    Given a rectangle's lower left and upper right corners, compute the points
    to create round corners and return them.
    """
    verts = []
    # Corner left-bottom:
    if corners[0]:
        x_moved = x1 + value
        y_moved = y1 + value
        verts_round = drawArc(x_moved, y_moved, value, 4.71, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x1, y1))

    # Corner left-top:
    if corners[1]:
        x_moved = x1 + value
        y_moved = y2 - value
        verts_round = drawArc(x_moved, y_moved, value, 3.14, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x1, y2))

    # Corner right-top:
    if corners[2]:
        x_moved = x2 - value
        y_moved = y2 - value
        verts_round = drawArc(x_moved, y_moved, value, 1.57, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x2, y2))

    # Corner right-bottom:
    if corners[3]:
        x_moved = x2 - value
        y_moved = y1 + value
        verts_round = drawArc(x_moved, y_moved, value, 0.0, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x2, y1))

    return verts


def convertColorValuesToFloat(content):
    """
    Convert color values to float, having max value of 1.0. Couldn't figure a way to do
    using PyPNG, could be possible.
    """
    content_temp = [[0 for x in range(len(content[0]))]
                    for y in range(len(content))]
    height = len(content[0])
    for i in range(len(content)):
        for j in range(height):
            content_temp[i][j] = float(content[i][j]) / 255
    return content_temp
