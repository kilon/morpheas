"""
Some necessary functions for Morpheas to work correctly.
"""

import math
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import bpy_extras


def drawRegion(points, color):
    """
    Draw a simple shape with given points and color.
    """
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

    # indices = [(i, i+1, i+2) for i in range(0, len(points)-2)]

    batch = batch_for_shader(
        shader, 'TRI_FAN', {"pos": points})

    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)


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


def pointsDistance(point1x, point1y, point2x, point2y):
    """
    Given two points on the plane, return their distance.
    """
    distance = math.sqrt(((point1x-point2x)**2)+((point1y-point2y)**2))
    return distance


def collisionDetect(x1, y1, x2, y2, w1, h1, w2, h2):
    """
    Given x and y of two rectangles and their width and height detect if
    they collide.
    """
    if x1 > x2 and x1 < x2 + w2 or x1 + w1 > x2 and x1 + w1 < x2 + w2:
        if y1 > y2 and y1 < y2 + h2 or y1 + h1 > y2 and y1 + h1 < y2 + h2:
            return True
