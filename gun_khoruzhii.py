import math
import time
from random import choice, randint as rnd
from tkinter import *

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
points = 0

x_t_min = 300
x_t_max = 700
y_t_min = 100
y_t_max = 500


canvas.create_rectangle(x_t_min, y_t_min, x_t_max, y_t_max)
label = Label(text="User: " + "Kirill" + ", score = " + str(points),
              font='Courier 20')
label.pack()


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
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
            self.vy = -self.vy / 2
            self.vx = self.vx / 2
            self.y = 550
            if self.live < 0:
                balls.pop(balls.index(self))
                canvas.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
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
        self.id = canvas.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450, 20 + max(self.f2_power, 20) * math.cos(self.an),
                      450 + max(self.f2_power, 20) * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


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


t1 = Target(1)
t2 = Target(2)

# t = list([x.live() for x in ])
screen1 = canvas.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global Gun, targets, screen1, balls, bullet
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', g1.fire2_start)
    canvas.bind('<ButtonRelease-1>', g1.fire2_end)
    canvas.bind('<Motion>', g1.targetting)
    z = 0.03
    t1.new_target()
    t2.new_target()
    t1.live = 1
    t2.live = 1
    while (t1.live and t2.live) or balls:
        for b in balls:
            b.move()
            if b.hit_test(t1) and t1.live:
                t1.live = 0
                t1.hit(point=2)
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(
                    screen1,
                    text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
            elif b.hit_test(t2) and t2.live:
                t2.live = 0
                t2.hit(point=3)
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(
                    screen1,
                    text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        t1.update()
        t2.update()
        canvas.update()

        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canvas.itemconfig(screen1, text='')

    canvas.delete(Gun)

    root.after(750, new_game)


new_game()


def tick():
    """ Обновление счёта игрока """
    label.config(
        text="User: " + "Kirill" + ", score = " + str(points),
        font='Courier 20')
    label.after(200, tick)


label.after_idle(tick)

root.mainloop()
