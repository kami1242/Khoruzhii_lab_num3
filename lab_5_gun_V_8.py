# Game:     "GUN" V8
# Author:   Khoruzhii Kirill


import math
import time
from random import choice, randint as rnd
from tkinter import *


# Создание поля:
root = Tk()
root.title("GUN 3.0")
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='#ECD5E3')
canvas.pack(fill=BOTH, expand=1)


# Константы игры:
points = 0
phase0 = 0
delta = 200  # сдвиг создания мишеней
x_t_min = 0  # границы мешеней
x_t_max = 800
y_t_min = 0
delta_r = 0  # случайное движение шариков
y_t_max = 600
v_t_min = -30
v_t_max = 50

r_t_min = 10
r_t_max = 20
N = 5

v_gun = 5
y_gun_0 = 100
x_gun_0 = 50
stop = 1.5  # потеря скорости на границе


# Цвета в меню:
theme_text_color = '#ADF1D2'
theme_fill_color = '#50808E'
theme_color = '#222e50'
theme_outline_color = '#ADF1D2'


# Подпись
name = ''
FF = 1

ent = Entry(width=20)
ent.pack(side=RIGHT)

label = Label(text="score = " + str(points) + ", User: " + name,
              font='Courier 20')
label.pack(side=RIGHT)

but_next = Button(text="Next")
#but_next.pack(side=LEFT)

but_name = Button(text="Save your name")
#but_name.pack(side=LEFT)


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = rnd(1, 200) / 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['#FFCCB6', '#CBAACB', '#FF968A', '#55CBCD'])
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 20

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        if self.y <= 550:
            self.vy -= 1.1
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        else:
            self.vy = -self.vy / stop
            self.vx = self.vx / stop
            self.y = 550
            if self.live < 0:
                balls.pop(balls.index(self))
                canvas.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / stop
            self.x = 780
        if self.x < 0:
            self.vx = -self.vx / stop
            self.x = 0
        if self.y < 0:
            self.vy = -self.vy
            self.y = 0

    def hit_test(self, ob):
        flag = (abs(ob.x - self.x) <= (self.r + ob.r)) and (
            abs(ob.y - self.y) <= (self.r + ob.r))
        return flag


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.vx = 0
        self.vy = 0
        self.x = x_gun_0
        self.y = y_gun_0

        self.id = canvas.create_line(
            self.x, self.y,
            self.x + 10, self.y + 10, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча
        vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.x, self.y)
        new_ball.r += rnd(1, 500) / 100
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - self.y) / (event.x - self.x))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x, self.y, self.x +
                      max(self.f2_power, 20) *
                      math.cos(self.an),
                      self.y + max(self.f2_power, 20) *
                      math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')

    def Gun_to_down_P(self, event):
        g1.vy = v_gun

    def Gun_to_down_R(self, event):
        g1.vy = 0

    def Gun_to_up_P(self, event):
        g1.vy = -v_gun

    def Gun_to_up_R(self, event):
        g1.vy = 0

    def Gun_to_r_P(self, event):
        g1.vy = -v_gun

    def Gun_to_l_R(self, event):
        g1.vy = 0

    def Update(self):
        g1.y += self.vy
        g1.x += self.vx


class Target:
    def __init__(self, N):
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0, tag='targ' + str(N))
        self.new_target()
        self.vx = rnd(-v_t_min - N, v_t_max + N) / 10 + 1
        self.vy = rnd(-v_t_min - N, v_t_max + N) / 10 + 1

    def new_target(self):
        """ Инициализация новой цели. """
        r = self.r = rnd(r_t_min, r_t_max)
        x = self.x = rnd(x_t_min + r + delta, x_t_max - r)
        y = self.y = rnd(y_t_min + r, y_t_max - r)
        color = self.color = 'purple'
        if FF:
            canvas.coords(self.id, x - r, y - r, x + r, y + r)
            canvas.itemconfig(self.id, fill=color)

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        canvas.coords(self.id, -10, -10, -10, -10)
        points += point

    def update(self):
        """ Движение мишеней """
        if phase0 != 1000 and FF:
            if self.live:
                self.x += self.vx + rnd(-delta_r, delta_r)
                self.y += self.vy + rnd(-delta_r, delta_r)
                canvas.coords(self.id,
                              self.x - self.r, self.y - self.r,
                              self.x + self.r, self.y + self.r)
                canvas.itemconfig(self.id, fill=self.color)

                if self.x > x_t_max - self.r:
                    self.vx *= -1
                    self.x = x_t_max - self.r

                if self.y > y_t_max - 50 - self.r:
                    self.vy *= -1
                    self.y = y_t_max - 50 - self.r

                if self.x < x_t_min + self.r:
                    self.vx *= -1

                if self.y < y_t_min + self.r:
                    self.vy *= -1


def Next(event):
    '''
    Ручное обновление мишеней
    '''
    global targets, balls
    for b in balls:
        b.x = 300
        b.y = 300
        canvas.delete(b.id)
    for t in targets:
        t.live = 0
    new_game()

def Name(event):
    global name
    if ent.get():
        name = ent.get()
    else:
        name = 'empty_name'
        #print(name)


def new_game(event=''):
    '''
    1) Проверяет состояние меню (phase):
        1,2     -- ИГРА
        10,11   -- ИНСТРУКЦИЯ
        100,101 -- ТИТРЫ
    2) Запускает соответсвующие куски программы
    '''
    global Gun, targets, screen1, balls, bullet, points, phase0, g1
    if phase0 == 100:  # авторство
        phase0 = 101
    elif phase0 == 10:  # инструкция
        phase0 = 11
    elif phase0 == 1:
        for obj in theme:
            canvas.delete(obj)
        for obj in theme_2:
            canvas.delete(obj)
        screen1 = canvas.create_text(400, 300, text='', font='28')
        targets = []
        for i in range(N):
            targets.append(Target(i + 1))
        bullet = 0
        balls = []
        phase0 = 2
    elif phase0 == 2:
        FLAG = 1
        bullet = 0
        balls = []
        z = 0.03
        for t in targets:
            t.new_target()
        for t in targets:
            t.live = 1
        while FLAG or balls:
            for b in balls:
                b.move()
                for t in targets:
                    if b.hit_test(t) and t.live:
                        t.live = 0
                        t.hit(point=2)
                        canvas.itemconfig(
                            screen1,
                            text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
                        FLAG = 0

            for t in targets:
                if t.x - t.r < g1.x < t.x + t.r and (
                        t.y - t.r < g1.y < t.y + t.r):
                    final_0()
                t.update()

            g1.Update()
            canvas.update()

            time.sleep(0.03)
            g1.targetting()
            g1.power_up()
        canvas.itemconfig(screen1, text='')
        canvas.delete(Gun)
        for i in range(5):
            targets.append(Target(len(targets) + i + 1))

    root.after(1, new_game)


def tick():
    """ Обновление счёта игрока """
    label.config(
        text="score = " + str(points) + ", User: " + name,
        font='Courier 20')
    label.after(200, tick)


g1 = Gun()


# Привязка кнопок:
label.after_idle(tick)
but_next.bind('<Button-1>', Next)
but_name.bind('<Button-1>', Name)
root.bind('<KeyPress-Down>', g1.Gun_to_down_P)
root.bind('<KeyRelease-Down>', g1.Gun_to_down_R)
root.bind('<KeyPress-Up>', g1.Gun_to_up_P)
root.bind('<KeyRelease-Up>', g1.Gun_to_up_R)
canvas.bind('<Button-1>', g1.fire2_start)
canvas.bind('<ButtonRelease-1>', g1.fire2_end)
canvas.bind('<Motion>', g1.targetting)


# Блоки меню:
theme = []
theme_2 = []
theme_3 = []
theme_4 = []
theme.append(canvas.create_rectangle(
    x_t_min, y_t_min, x_t_max, y_t_max, fill=theme_color))


# Создание слайда меню:
def MENU_0():
    theme.append(canvas.create_rectangle(50, 50, 750, 50 + 100,
                                         fill=theme_fill_color,
                                         outline=theme_outline_color, width=4))
    theme.append(canvas.create_text(400, 100, text="ИГРАТЬ",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 60"))
    theme.append(canvas.create_text(700, 100, text="1",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 60"))
    theme.append(canvas.create_rectangle(50, 200, 750, 200 + 100,
                                         fill=theme_fill_color,
                                         outline=theme_outline_color, width=4))
    theme.append(canvas.create_text(400, 250, text="ИНСТРУКЦИЯ",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 40"))
    theme.append(canvas.create_text(700, 250, text="2",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 60"))
    theme.append(canvas.create_rectangle(50, 350, 750, 350 + 100,
                                         fill=theme_fill_color,
                                         outline=theme_outline_color, width=4))
    theme.append(canvas.create_text(400, 400, text="АВТОР",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 40"))
    theme.append(canvas.create_text(700, 400, text="3",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 60"))
    theme.append(canvas.create_rectangle(450, 500, 750, 550,
                                         fill=theme_fill_color,
                                         outline=theme_outline_color, width=4))
    theme.append(canvas.create_text(600, 525, text="!use keyboard!",
                                    fill=theme_text_color, justify=CENTER,
                                    font="Courier 20"))


MENU_0()

# Управление меню:


def ONE(event):
    global phase0
    phase0 = 1


def TWO(event):
    global phase0, theme_2
    if phase0 == 11:
        for obj in theme_2:
            canvas.delete(obj)
        phase0 = 0
        # print("TYT")
    else:
        phase0 = 10
        theme_2.append(canvas.create_rectangle(
            x_t_min, y_t_min, x_t_max, y_t_max, fill=theme_color))
        theme_2.append(canvas.create_text(
            400, 100, text="              ИНСТРУКЦИЯ                 ",
            fill=theme_text_color, justify=CENTER, font="Courier 40"))
        theme_2.append(canvas.create_text(
            400, 200, text="1) За попадание: +2 очка                 ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_2.append(canvas.create_text(
            400, 250, text="2) Каждый уровень: + 5 мишеней           ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_2.append(canvas.create_text(
            400, 300, text="3) При столкновение с мишенью: Конец Игры",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_2.append(canvas.create_text(
            400, 350, text="4) Press 'F' to... закончить игру        ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_2.append(canvas.create_text(
            400, 400, text="5) Press 'R' чтобы попробовать ещё раз   ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_2.append(canvas.create_text(
            400, 450, text="6) Press 'Enter' to save User's name     ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))

def THREE(event):
    global message, phase0
    if phase0 == 101:
        for obj in theme_3:
            canvas.delete(obj)
        phase0 = 0
    else:
        phase0 = 100
        theme_3.append(canvas.create_rectangle(
            x_t_min, y_t_min, x_t_max, y_t_max, fill=theme_color))
        theme_3.append(canvas.create_text(
            400, 200, text="Made by:                    ",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))
        theme_3.append(canvas.create_text(
            400, 250, text="              Хоружий Кирилл",
            fill=theme_text_color, justify=CENTER, font="Courier 20"))

# Обнуление некоторых функций:


def none_0():
    pass

# Конец игры:


def final_0():
    global phase0, targets, balls, FF
    for b in balls:
        b.x = 300
        b.y = 300
        b.vx = 0
        b.vy = 0
        canvas.delete(b.id)
    for t in targets:
        t.x = 500
        t.y = 300
        t.vx = 0
        t.vy = 0
        canvas.delete(t.id)
    
    theme_4.append(canvas.create_rectangle(
        x_t_min, y_t_min, x_t_max, y_t_max, fill=theme_color))
    theme_4.append(canvas.create_text(400, 200, text="Поздравляем " + name + ", Вы набрали:            ",
                                      fill=theme_text_color, justify=CENTER,
                                      font="Courier 20"))
    
    theme_4.append(canvas.create_text(
        400, 250,
        text="                            " + str(points) + " points!!!",
        fill=theme_text_color, justify=CENTER, font="Courier 20"))
    phase0 = 1000
    FF = 0
    canvas.bind('<Button-1>', none_0)
    canvas.bind('<ButtonRelease-1>', none_0)
    canvas.bind('<Motion>', none_0)


def FINAL(event):
    global phase0
    final_0()


def RESTART(event, flag = 1):
    global phase0, points, FF
    FF = 1
    for t in targets:
        canvas.delete(t.id)
    for b in balls:
        canvas.delete(b.id)
    for obj in theme:
        canvas.delete(obj)
    for obj in theme_2:
        canvas.delete(obj)
    for obj in theme_3:
        canvas.delete(obj)
    for obj in theme_4:
        canvas.delete(obj)
    canvas.itemconfig(screen1, text='')
    phase0 = 1
    points = 0
    if flag:
        new_game()
    canvas.bind('<Button-1>', g1.fire2_start)
    canvas.bind('<ButtonRelease-1>', g1.fire2_end)
    canvas.bind('<Motion>', g1.targetting)



root.bind('1', ONE)
root.bind('2', TWO)
root.bind('3', THREE)
root.bind('f', FINAL)
root.bind('r', RESTART)
root.bind('<Return>', Name)


# Запуск основного цикла:
new_game()
root.mainloop()
