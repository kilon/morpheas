import bpy
import bgl
import blf
import bpy_extras
import math


def drawRegion(mode, points, color):

    bgl.glColor4f(color[0], color[1], color[2], color[3])
    if mode == 'GL_LINE_LOOP':
        bgl.glBegin(bgl.GL_LINE_LOOP)
    else:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_POLYGON)

    # start with corner right-bottom
    for i in range(0, len(points)):
        bgl.glVertex2f(points[i][0], points[i][1])

    bgl.glEnd()


def drawArc(cx, cy, r, startAngle, arcAngle, numSegments):
    """Draw round corners, (cx, cy) center of circle, r strength value"""
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
    verts = []
    # Corner left-bottom
    if(corners[0]):
        x_moved = x1 + value
        y_moved = y1 + value
        verts_round = drawArc(x_moved, y_moved, value, 4.71, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x1, y1))

    # Corner left-top:
    if(corners[1]):
        x_moved = x1 + value
        y_moved = y2 - value
        verts_round = drawArc(x_moved, y_moved, value, 3.14, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x1, y2))

    # Corner right-top:
    if(corners[2]):
        x_moved = x2 - value
        y_moved = y2 - value
        verts_round = drawArc(x_moved, y_moved, value, 1.57, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x2, y2))

    # Corner right-bottom:
    if(corners[3]):
        x_moved = x2 - value
        y_moved = y1 + value
        verts_round = drawArc(x_moved, y_moved, value, 0.0, -1.57, steps)
        for i in verts_round:
            verts.append(i)
    else:
        verts.append((x2, y1))

    return verts

# Convert color values to float, having max value of 1.0. Couldn't figure a way to do
# using PyPNG, could be possible.


def convertColorValuesToFloat(content):
    content_temp = [[0 for x in range(len(content[0]))]
                    for y in range(len(content))]
    height = len(content[0])
    for i in range(len(content)):
        for j in range(height):
            content_temp[i][j] = float(content[i][j]) / 255
    return content_temp
