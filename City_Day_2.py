from graph import *
import math


def ellipse(xc, yc, a, b):
    # xc, yc - coords of the center, a, b - semimajor axises
    changeCoords(circle(0, 0, 10), [(xc - a, yc - b), (xc + a, yc + b)])


def car(x, y, w, h):  # x, y - coords of the corner, w - width, h - height
    # exhaust pipe
    penColor("black")
    brushColor("black")
    ellipse(x + 0, y + h * 40 / 60, w * 20 / 180, h * 5 / 60)

    # body
    penColor("OrangeRed")
    brushColor('OrangeRed')
    rectangle(x + w * 30 / 180, y + 0, x + w * 100 / 180, y + h * 20 / 60)
    rectangle(x + 0, y + h * 20 / 60, x + w * 180 / 180, y + h * 50 / 60)
    penColor("white")
    brushColor("white")
    rectangle(x + w * 35 / 180, y + h * 5 / 60,
              x + w * 60 / 180, y + h * 20 / 60)
    rectangle(x + w * 70 / 180, y + h * 5 / 60,
              x + w * 95 / 180, y + h * 20 / 60)

    # wheels
    penColor("black")
    brushColor("black")
    ellipse(x + w * 40 / 180, y + h * 50 / 60, w * 20 / 180, h * 15 / 60)
    ellipse(x + w * 140 / 180, y + h * 50 / 60, w * 20 / 180, h * 15 / 60)


def windows(x1, y1, x2, y2, step, color):
    penSize(8)
    penColor(color)
    for x_w in range(0, int((x2 - x1) / step), 2):
        for y_w in range(0, int((y2 - y1) / step), 2):
            line(x_w * step + x1, y_w * step + y1,
                 x_w * step + step + x1, y_w * step + y1)


def clouds(x1, y1, x2, y2):
    for i in range(3):
        penColor(200 + 11 * i, 200 + 11 * i, 200 + 11 * i)
        brushColor(200 + 11 * i, 200 + 11 * i, 200 + 11 * i)
        ellipse(x1, y1, x2 / (i / 2 + 1), y2 / (i / 2 + 1))


def background(x, y, w, h):
    # general background
    penColor(100, 100, 100)
    brushColor(100, 100, 100)
    rectangle(x, y, x + w, y + h)

    penSize(5)
    penColor("white")
    brushColor('DeepSkyBlue')
    rectangle(x, y, x + w, y + h * 9 / 15)
    penSize(1)

    #buildings and clouds
    penColor(130, 130, 130)
    brushColor(130, 130, 130)
    rectangle(x + w * 6 / 9, y + h * 1 / 15, x + w * 8 / 9, y + h * 10 / 15)
    windows(x + w * 6 / 9 + 6, y + h * 1 / 15 + 10,
            x + w * 8 / 9, y + h * 10 / 15, 9, 'Pink')

    clouds(x + w * 6 / 9, y + h * 3 / 15, w / 2, h / 10)

    penColor('Gainsboro')
    brushColor('white')
    clouds(x + w * 2 / 9, y + h * 4 / 15, w / 2, h / 10)

    penColor(130, 150, 130)
    brushColor(130, 150, 130)

    penColor(130, 130, 150)  # left one
    brushColor(130, 130, 150)
    rectangle(x + w * 0.5 / 9, y + h * 0.5 / 15,
              x + w * 2.5 / 9, y + h * 9.5 / 15)
    windows(x + w * 0.5 / 9 + 5, y + h * 0.5 / 15 + 10,
            x + w * 2.5 / 9 + 5, y + h * 9.5 / 15 + 10, 10, 'Lime')

    penColor(100, 100, 100)
    brushColor(100, 100, 100)
    rectangle(x + w * 3 / 9, y + h * 2 / 15, x + w * 5 / 9, y + h * 10 / 15)
    windows(x + w * 3 / 9 + 10, y + h * 2 / 15 + 10,
            x + w * 5 / 9, y + h * 10 / 15, 7, 'Yellow')

    penColor(160, 160, 160)
    brushColor(160, 160, 160)
    rectangle(x + w * 2 / 9, y + h * 4 / 15 - 15,
              x + w * 4 / 9, y + h * 11 / 15 - 15)
    windows(x + w * 2 / 9 + 10, y + h * 4 / 15 - 15 + 10,
            x + w * 4 / 9, y + h * 11 / 15 - 15, 8, 'Pink')


background(250, 0, 250, 300)
background(250, 300, 250, 300)
background(0, 0, 250, 300)
background(0, 300, 250, 300)


def markup(start, step):
    penSize(4)
    penColor('white')
    for x_s in range(0, 500 // step, 2):
        line(x_s * step, start, x_s * step + step, start)


markup(520, 20)
markup(250, 10)
markup(560, 20)

car(450, 520, -180, 60)
car(50, 500, 180, 60)
car(300, 250, -90, 30)
car(450, 220, -90, 30)
car(140, 220, -90, 30)

run()
