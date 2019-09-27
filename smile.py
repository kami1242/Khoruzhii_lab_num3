from graph import *
import math as m

a = 20
z = 200
w = 11

brushColor('yellow')
circle(z, z, 5 * a)

brushColor('black')
# x1 y1 x2 y2
rectangle(z - 3 * a, z + 3 * a, z + 3 * a, z + 2 * a)

brushColor('red')
circle(z - 2.5 * a, z - 1.5 * a, a*1.2)
circle(z + 2 * a, z - 1.5 * a, a/1.1)
brushColor('black')
circle(z - 2.2 * a, z - 1.5 * a, a/3)
circle(z + 2.2 * a, z - 1.5 * a, a/2.6)


def rot(x_r, y_r, f_r):
    f_r = f_r / 180 * m.pi
    xy = [x_r, y_r]
    xy = [xy[0] * m.cos(f_r) - xy[1] * m.sin(f_r), xy[0]
          * m.sin(f_r) + xy[1] * m.cos(f_r)]
    return(xy)

#xy1 = rot(2*a, a/4, f)
#xy2 = rot(2*a, -a/4, f)
#xy3 = rot(-a*2, -a/4, f)
#xy4 = rot(-a*2, a/4, f)
#points = [(xy1[0]+zl+25, xy1[1]+zl), (xy2[0]+zl+25, xy2[1]+zl), 
#	(xy3[0]+zl, xy3[1]+zl), (xy4[0]+zl, xy4[1]+zl)]
#polygon(points)

penSize(w)
line(z+a/2, z-1.2*a, z+4*a, z-4*a)
penSize(w+2)
line(z-a/2, z-1.2*a, z-4*a, z-4*a)

run()
