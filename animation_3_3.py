from graph import *
import math as m
from random import randint

brushColor('green')
rectangle(0, 300, 600, 600)
brushColor('#FFF5EE')
rectangle(0, 0, 600, 300)
xc1, yc = 200, 450
M = 150
step = -20
R = 200
phi = 0
ufox = 50
ufoy = 50
dx = 0


def ellips(x, y, a, b, f):
    f = f * m.pi / 180
    x_e = [i for i in range(-a, a)]
    y1, y2 = [], []
    for i in range(len(x_e)):
        xy1 = [x_e[i], b * (1 - (x_e[i] / a)**2)**0.5]
        xy2 = [x_e[i], -b * (1 - (x_e[i] / a)**2)**0.5]
        xy1 = [xy1[0] * m.cos(f) - xy1[1] * m.sin(f), xy1[0]
               * m.sin(f) + xy1[1] * m.cos(f)]
        xy2 = [xy2[0] * m.cos(f) - xy2[1] * m.sin(f), xy2[0]
               * m.sin(f) + xy2[1] * m.cos(f)]
        y1.append((xy1[0] + x, xy1[1] + y))
        y2.append((xy2[0] + x, xy2[1] + y))
    y2 = y2[::-1]
    polygon(y1 + y2)


def ufo(x, y, size):
    penSize(0)
    brushColor(210, 250, 210)
    penColor(210, 250, 210)
    light = []
    light.append((x, y))
    light.append((x - 20 * size, y + 20 * size))
    light.append((x + 20 * size, y + 20 * size))
    polygon(light)
    brushColor(168, 168, 168)
    penColor(168, 168, 168)

    ellips(x, y, 20 * size, 5 * size, 0)

    brushColor(180, 220, 220)
    penColor(180, 220, 220)
    ellips(x, y - 3 * size, 12 * size, 4 * size, 2)
    brushColor('white')
    penColor('white')
    ellips(x, y + 3 * size, 3 * size, 1 * size, -5)
    ellips(x - 8 * size, y + 2 * size, 3 * size, 1 * size, 0)
    ellips(x + 8 * size, y + 2 * size, 3 * size, 1 * size, 5)
    ellips(x - 14 * size, y + 0.05 * size, 3 * size, 1 * size, -5)
    ellips(x + 14 * size, y + 0.05 * size, 3 * size, 1 * size, 0)


def keyPressed(event):
    global dx, dy
    if event.keycode == VK_ESCAPE:
        close()
    if event.keycode == VK_LEFT:
        dx = -5
        dy = 0
    elif event.keycode == VK_RIGHT:
        dx = 5
        dy = 0


def up_ufo():
    for i in range(3):
        moveObjectBy(L[i], dx, randint(1, 5) - 3)
        changeFillColor(L[i], randColor())


def update0():
    moveObjectBy(obj0, 0, step)
    if yCoord(obj0) <= M:
        moveObjectBy(obj0, 0, yc - M + randint(1, R))


def update1():
    moveObjectBy(obj1, 0, step)
    if yCoord(obj1) <= M:
        moveObjectBy(obj1, 0, yc - M + randint(1, R))


def update2():
    moveObjectBy(obj2, 0, step)
    if yCoord(obj2) <= M:
        moveObjectBy(obj2, 0, yc - M + randint(1, R))


def update3():
    moveObjectBy(obj3, 0, step)
    if yCoord(obj3) <= M:
        moveObjectBy(obj3, 0, yc - M + randint(1, R))


def update4():
    moveObjectBy(obj4, 0, step)
    if yCoord(obj4) <= M:
        moveObjectBy(obj4, 0, yc - M + randint(1, R))


def update5():
    moveObjectBy(obj5, 0, step)
    if yCoord(obj5) <= M:
        moveObjectBy(obj5, 0, yc - M + randint(1, R))


def update6():
    moveObjectBy(obj6, 0, step)
    if yCoord(obj6) <= M:
        moveObjectBy(obj6, 0, yc - M + randint(1, R))


canvasSize(600, 600)
windowSize(600, 600)

x = 100
y = 100

obj0 = image(0, randint(1, R), "cow.png")
obj1 = image(100, randint(1, R), "cow.png")
obj2 = image(200, randint(1, R), "cow.png")
obj3 = image(300, randint(1, R), "cow.png")
obj4 = image(400, randint(1, R), "cow.png")
obj5 = image(500, randint(1, R), "cow.png")
obj6 = image(600, randint(1, R), "cow.png")

ufo(100, 50, 7)
ufo(350, 50, 7)
ufo(600, 50, 7)

brushColor('red')
MAIN1 = circle(200, 200, 20)
MAIN2 = circle(230, 200, 20)
MAIN3 = circle(260, 200, 20)
L = [MAIN1, MAIN2, MAIN3]
#moveObjectBy(MAIN1, 10, 10)

onKey(keyPressed)
onTimer(update0, 50)
onTimer(update1, 50)
onTimer(update2, 50)
onTimer(update3, 50)
onTimer(update4, 50)
onTimer(update5, 50)
onTimer(update6, 50)

onTimer(up_ufo, 50)

for i in range(12):
    image(-50 + 60 * i, 500, "cow.png")

run()
