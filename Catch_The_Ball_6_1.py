# Хоружий Кирилл
# Игра: "Поймай шарик" -- V1
# 18.10.2019

from tkinter import *
from random import randrange as rnd
import numpy as np

# Оформление полотна:
root = Tk()
root.geometry('800x600')
canv = Canvas(root, bg='#000099')
canv.pack(fill=BOTH, expand=1)

# Задаём цвета шариков и их количество (N <= len(colors)):
N = 9
colors = [
    '#FFB5E8', '#ABDEE6', '#FFFFB5',
    '#FFCCB6', '#CBAACB', '#FF968A',
    '#55CBCD', '#97C1A9', '#ECD5E3']


# Стартовые условия игры:
score = 0           # начальный счёт игрока
lvl = 0	 			# увеличение скорости шариков

x_min = 100         # расположение по x
x_max = 700

y_min = 100         # расположение по у
y_max = 500

r_min = 20          # макс и мин радиусы
r_max = 50

x_border_min = 50   # граничные условия для шариков
x_border_max = 750

y_border_min = 50
y_border_max = 500


# Создание массива скоростей шариков:
vx = np.array([rnd(-5, 5) for i in range(N)])
vy = np.array([rnd(-5, 5) for i in range(N)])


# Создание "особенного" шарика:
vx[N - 1] = 7
vy[N - 1] = 7
colors[N - 1] = 'black'


# Функционал программы:
def new_ball():
    ''' создаёт N шариков в заданных рамках '''
    global x, y, r
    x = np.array([rnd(x_min, x_max) for i in range(N)])
    y = np.array([rnd(y_min, y_max) for i in range(N)])
    r = np.array([rnd(r_min, r_max) for i in range(N)])
    for i in range(N):
        canv.delete('ball')
        canv.create_oval(
            x[i] - r[i], y[i] - r[i],
            x[i] + r[i], y[i] + r[i],
            fill='white', width=0,
            activefill='red', tag='ball' + str(i))


def update():
    '''  обновление местоположения N шариков'''
    global x, y, vx, vy
    x += vx
    y += vy
    for i in range(N):
        # чтобы изображение мяча не выходилао за рамку по x
        if x[i] > 750:
            vx[i] *= -1
            x[i] = 750
        if x[i] < 50:
            vx[i] *= -1
            x[i] = 50

        # чтобы изображение мяча не выходилао за рамку по y
        if y[i] > 500:
            vy[i] *= -1
            y[i] = 500
        if y[i] < 50:
            vy[i] *= -1
            y[i] = 50

        canv.delete('ball' + str(i))
        canv.create_oval(x[i] - r[i], y[i] - r[i],
                         x[i] + r[i], y[i] + r[i],
                         fill=colors[i], activefill='red',
                         tag='ball' + str(i))

    root.after(15, update)


def click(event):
    ''' фиксирует щелчок мышкой и проверяет условие
        попадания в ближайший шарик '''
    global score
    x_e = event.x
    y_e = event.y
    rho = (x - x_e)**2 + (y - y_e)**2
    n = rho.tolist().index(min(rho))
    if min(rho) <= r[n]**2:
        # проверка на успех с особенным шариком
        if n == N - 1:
            score += 10
            r[n] -= 2
            vx[n] += lvl
            vy[n] += lvl
        else:
            score += 2
            vx[n] = rnd(-5 - lvl, 5 + lvl)
            vy[n] = rnd(-5 - lvl, 5 + lvl)
        x[n] = rnd(y_min, y_max)
        y[n] = rnd(y_min, y_max)


# Цикл игры:
new_ball()
update()


# Обновление счёта игрока
def tick():
    label.config(text="Score = " + str(score),
                 font='Courier 20')
    label.after(200, tick)


label = Label(text=str(rnd(100, 200)),
              font='Courier 20')
label.pack()
label.after_idle(tick)


# Обновление системы на нажатие СКМ:
def OFF(event):
    global score
    new_ball()
    score = 0
    lvl = 0
    r[N - 1] = 30


# Штраф за неаккуратность по двойному нажатию
def ALARM(event):
    global score
    score -= 1


# Усложнение по ПКМ
def LVL_UP(event):
    global lvl
    lvl += 1


# Привязка клавиш:
canv.bind('<Button-1>', click)
canv.bind('<Button-2>', OFF)
canv.bind('<Button-3>', LVL_UP)
canv.bind('<Double-Button-1>', ALARM)

# Запуск цикла:
root.mainloop()
