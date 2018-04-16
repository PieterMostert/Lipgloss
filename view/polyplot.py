# LIPGLOSS - Graphical user interface for constructing glaze recipes
# Copyright (C) 2017 Pieter Mostert

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# version 3 along with this program (see LICENCE.txt).  If not, see
# <http://www.gnu.org/licenses/>.

# Contact: pi.mostert@gmail.com

# Useful references:
# http://infohost.nmt.edu/tcc/help/pubs/tkinter//canvas.html
# http://www.tcl.tk/man/tcl8.5/TkCmd/canvas.htm
# Ref: canvassimple.py
# http://tkinter.unpythonic.net/wiki/A_tour_of_Tkinter_widgets
 
from tkinter import *
from tkinter import ttk  
from math import log10, floor
from functools import partial

#style = Style()

def stepsize(interval):
    ri = 10**floor(log10(interval))
    if interval/ri < 2:
        return ri
    elif interval/ri < 5:
        return 2*ri
    else:
        return 5*ri

def ticks(a,b):   #Unless a and b are too close together, generates an arithmetic seq of between 6 and 12 points,
                  #with the first being roughly a, and the last being roughly b.  
    ss = stepsize(max((b-a)/4, 0.01))
    p = ss*floor(a/ss)
    return [round(p+ss*k,8) for k in range(floor((b-p)/ss)+2)]
    #return pts

def create_polygon_plot(self, data, scaling):
        
    plotFont = ('Helv', 12)
    
    self.width = eval(self.config('width')[4])
    self.height = eval(self.config('height')[4])

    x_pts = [p[0] for p in data]
    y_pts = [p[1] * scaling for p in data]
    x_min = min(x_pts)
    y_min = min(y_pts)
    x_max = max(x_pts)
    y_max = max(y_pts)
    delta_x = x_max - x_min
    delta_y = y_max - y_min

    d1x = 80
    d1y = 50
    d2 = 30
    s = max(delta_x/(self.width-d1x-d2-10), delta_y/(self.height-d1y-d2-10))

    x0 = max(0,x_min/s - 10)
    y0 = max(0,y_min/s - 10)

    x_ticks = [t for t in ticks(x_min,x_max) if t/s>=x0]
    y_ticks = [t for t in ticks(y_min/scaling,y_max/scaling) if t/s*scaling>=y0]

    data1 = [(px / s, -py / s * scaling) for px, py in data]

    pgon = self.create_polygon(data1, fill = 'green', outline = 'green')

    self.point = self.create_oval(-d1x, -d1y - 6, -d1x - 6, -d1y, fill = "red", outline = 'red')
    self.show_pos = self.create_text(self.width + x0 - d1x - 70, -self.height + d1y - y0 + 30, text='', font=plotFont)

    def showxy(event):
        xm = event.x
        ym = event.y
        str1 = "x=%.2f, y=%.2f" % (s * (xm - d1x+x0), -s / scaling * (ym - self.height + d1y - y0))
        self.itemconfig(self.show_pos, text=str1)
        self.coords(self.point,[xm - 3, ym - 3, xm + 3, ym + 3])

    def hide_point(event):
        self.itemconfig(self.point, state='hidden')
        self.itemconfig(self.show_pos, state='hidden')

    def show_point(event):
        self.itemconfig(self.point, state='normal')
        self.itemconfig(self.show_pos, state='normal')
            
    # create axes
    x_axis = self.create_line(x0, -y0, self.width - d2 + x0 - d1x, -y0, width=1)  #x-axis
    y_axis = self.create_line(x0, -y0, x0, -y_ticks[-1]/s*scaling, width=1)  #y-axis

    # create x-axis labels
    for x in x_ticks:
        xs = x/s
        self.create_line(xs, -y0, xs, -y0 - 5, width=2)
        self.create_text(xs, -y0 + 4, text='{}'.format( (x) ),
                      anchor='n', font=plotFont)
     
    # create y-axis labels
    for y in y_ticks:
        ys = -y/s*scaling
        self.create_line(x0, ys, x0 + 5, ys, width=2)
        self.create_text(x0-4, ys, text='{}'.format( (y)  ),
                      anchor='e', font=plotFont)
     
    self.move("all", d1x - x0, self.height - d1y + y0)
  
    self.bind("<Motion>", showxy)
    self.bind("<Leave>", hide_point)
    self.bind("<Enter>", show_point)
    self.config(cursor = "none")

Canvas.create_polygon_plot = create_polygon_plot

if 0==1:
    root = Tk()
    window = Frame(root)
    window.grid()
    dat = [[20, 94], [33, 98], [32, 120], [61, 180],[75,160],[398,223]]

    can = Canvas(window, width=300, height=300)

    can.grid(column=2)
    can.create_polygon_plot(dat, 0.52)

    root.mainloop()

