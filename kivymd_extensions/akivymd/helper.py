from math import cos, radians, sin


def point_on_circle(degree, center, dis):
    """
    Finding the x,y coordinates on circle, based on given angle
    """

    if 0 <= degree <= 90:
        degree = 90 - degree
    elif 90 < degree < 360:
        degree = 450 - degree

    radius = dis
    angle = radians(degree)

    x = center[0] + (radius * cos(angle))
    y = center[1] + (radius * sin(angle))

    return [x, y]
