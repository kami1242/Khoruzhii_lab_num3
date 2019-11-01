import math
import time
from random import choice, randint as rnd
from tkinter import *

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='#ECD5E3')
canvas.pack(fill=BOTH, expand=1)
points = 0

x_t_min = 50  # границы мешеней
x_t_max = 700
y_t_min = 000
y_t_max = 600

v_gun = 5
y_gun_0 = 100
x_gun_0 = 100
stop = 1.5  # потеря скорости на границе


canvas.create_rectangle(x_t_min, y_t_min, x_t_max, y_t_max)
label = Label(text="User: " + "Kirill" + ", score = " + str(points),
              font='Courier 20')
label.pack(side=RIGHT)

but_next = Button(text="Next")
but_next.pack(side=LEFT)


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
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
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

    def Update(self):
        g1.y += self.vy
        g1.x += self.vx


class Target:
    def __init__(self, N):
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0, tag='targ' + str(N))
        self.new_target()
        self.vx = rnd(-3, 3)
        self.vy = rnd(-3, 3)

    def new_target(self):
        """ Инициализация новой цели. """
        r = self.r = rnd(10, 50)
        x = self.x = rnd(x_t_min + r, x_t_max - r)
        y = self.y = rnd(y_t_min + r, y_t_max - r)
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        canvas.coords(self.id, -10, -10, -10, -10)
        points += point

    def update(self):
        if self.live:
            self.x += self.vx
            self.y += self.vy
            canvas.coords(self.id,
                          self.x - self.r, self.y - self.r,
                          self.x + self.r, self.y + self.r)
            canvas.itemconfig(self.id, fill=self.color)

            if self.x > x_t_max - self.r:
                self.vx *= -1

            if self.y > y_t_max - self.r:
                self.vy *= -1

            if self.x < x_t_min + self.r:
                self.vx *= -1

            if self.y < y_t_min + self.r:
                self.vy *= -1


def Next(event):
    global t1, t2
    t1.live = 0
    t2.live = 0
    new_game()


t1 = Target(1)
t2 = Target(2)
t3 = Target(3)
t4 = Target(4)
t5 = Target(5)
t6 = Target(6)
t7 = Target(7)
t8 = Target(8)

targets = [t1, t2, t3, t4, t5, t6, t7, t8]


# t = list([x.live() for x in ])
screen1 = canvas.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global Gun, targets, screen1, balls, bullet, points
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
                points = -100
            t.update()

        g1.Update()
        canvas.update()

        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canvas.itemconfig(screen1, text='')

    canvas.delete(Gun)

    root.after(750, new_game)


def tick():
    """ Обновление счёта игрока """
    label.config(
        text="User: " + "Kirill" + ", score = " + str(points),
        font='Courier 20')
    label.after(200, tick)


label.after_idle(tick)
but_next.bind('<Button-1>', Next)
root.bind('<KeyPress-Down>', g1.Gun_to_down_P)
root.bind('<KeyRelease-Down>', g1.Gun_to_down_R)
root.bind('<KeyPress-Up>', g1.Gun_to_up_P)
root.bind('<KeyRelease-Up>', g1.Gun_to_up_R)
canvas.bind('<Button-1>', g1.fire2_start)
canvas.bind('<ButtonRelease-1>', g1.fire2_end)
canvas.bind('<Motion>', g1.targetting)


new_game()

root.mainloop()
