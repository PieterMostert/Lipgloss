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

from tkinter import *
from tkinter import ttk
from vert_scrolled_frame import *
import tkinter.messagebox

root = Tk()
root.title("LIPGLOSS")  # LInear Programming GLaze Oxide Software System. Terrible acronym, though it also happens to be a song by Pulp.
        
# Create the outer content frames
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create menubar
menubar = Menu(root)

# Create the selection window
selection_window = ttk.Frame(root, padding=(5, 5, 12, 12), borderwidth = 2, relief = 'solid') #shows list of ingredients and other possible restrictions

# Create the ingredient selection window
ingredient_selection_window = ttk.Frame(selection_window, padding=(5, 5, 5, 5)) # shows list of ingredients
select_ing_label = Label(ingredient_selection_window, text='Select ingredients', font = ('Helvetica',10))  # Heading

# Create the other selection window
other_selection_window = ttk.Frame(selection_window, padding=(5, 5, 5, 5)) # shows list of other restrictions
select_other_label = Label(other_selection_window, text='Select other restrictions', font = ('Helvetica',10))  # Heading
    
# Create the main window for entering and displaying restrictions
main_frame = ttk.Frame(root, padding=(5, 5, 12, 0))
main_frame['borderwidth'] = 2
main_frame['relief'] = 'solid'

recipe_name_frame = ttk.Frame(main_frame, padding=(5, 5, 12, 12)) # window for displaying the current recipe's name
restriction_frame = ttk.Frame(main_frame, padding=(5, 5, 12, 12)) # window for entering restrictions
restriction_sf = VerticalScrolledFrame(restriction_frame)
restriction_sf.frame_height = 500
Label(master=restriction_sf.interior).grid(row=9000) # A hack to make sure that when a new 'other restriction' is added,
                                                      # you don't have to scroll down to see it.
calc_frame = ttk.Frame(main_frame, padding=(15, 5, 10, 5))      # window holding the Calc button
message_frame = ttk.Frame(main_frame, padding=(15, 5, 10, 5))   # window displaying messages. At the moment, this isn't used

proj_frame = ttk.Frame(root, padding=(15, 5, 10, 5))            # window holding canvas displaying the 2-d projection

variable_info = ttk.Frame(proj_frame)
proj_canvas = Canvas(proj_frame, width=450, height=450, bg='white', borderwidth=1, relief='solid')

x_lab = Label(variable_info, text='x variable: Click right restriction name to select')
y_lab = Label(variable_info, text='y variable: Click left restriction name to select')

option_menu = Menu(menubar, tearoff=0)                 # create a pulldown menu, and add it to the menu bar

vsf = VerticalScrolledFrame(ingredient_selection_window)
vsf.frame_height = 400

# GRID REMAINING WIDGETS

# grid selection window
selection_window.pack(side='left',fill=Y)
ingredient_selection_window.grid(column = 0, row = 1, sticky = 'n')
other_selection_window.grid(column = 0, row = 2, sticky = 'n')

# grid the selection labels
for label in [select_ing_label, select_other_label]:
    label.grid(column=0, row=0, columnspan=2)

# grid the vertical scrolled frame containing the ingredients
vsf.grid()

# grid main frame
main_frame.pack(side='left', fill='y')
recipe_name_frame.grid(row = 0)
restriction_frame.grid(row = 10)
restriction_sf.pack()

# grid oxide part of restriction frame
oxide_heading_frame = ttk.Frame(restriction_sf.interior)
oxide_heading_frame.grid(row = 0, column = 0, columnspan = 7)
Label(oxide_heading_frame, text = 'Oxides', font = ('Helvetica', 12)).grid(column = 0, row = 0, columnspan = 3)

# grid ingredient part of restriction frame
ingredient_heading_frame = ttk.Frame(restriction_sf.interior)
ingredient_heading_frame.grid(row = 100, column = 0, columnspan = 7)
Label(ingredient_heading_frame, text = 'Ingredients', font = ('Helvetica', 12)).grid()

# grid other part of restriction frame
other_heading_frame = ttk.Frame(restriction_sf.interior)
other_heading_frame.grid(row = 1000, column = 0, columnspan = 7)
Label(other_heading_frame, text = 'Other', font = ('Helvetica', 12)).grid()

# grid calc frame
calc_frame.grid(row = 1)

# grid message frame. At the moment, this isn't used
message_frame.grid(row = 3)

# grid 2d projection frame
proj_frame.pack(side='right', fill='y') #grid(column = 1, row = 1, rowspan=1000, sticky = 'nw')
variable_info.grid(row=0)
proj_canvas.grid(row=1)
x_lab.grid(row=0, sticky=W)
y_lab.grid(row=1, sticky=W)

