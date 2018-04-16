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

import tkinter as tk
from tkinter import ttk
import os
from inspect import getsourcefile
from os.path import abspath, dirname
from functools import partial
#from model.lipgloss.recipes import Recipe        # eliminate this

try:
    from .vert_scrolled_frame import VerticalScrolledFrame
    from .pretty_names import prettify, pretty_entry_type
    from .polyplot import *
except ImportError:
    from vert_scrolled_frame import VerticalScrolledFrame
    from pretty_names import prettify
    from polyplot import *

import tkinter.messagebox
import shelve

def open_recipe_menu():
    pass

def save_recipe():
    pass

def save_new_recipe():
    pass

def edit_oxides():
    pass

def edit_other_restrictions():
    pass

def restriction_settings():
    pass

class MainWindow:

    def __init__(self):
        self.root = Tk()
        self.root.title("LIPGLOSS")  # LInear Programming GLaze Oxide Software System. Terrible acronym, though it also happens to be a song by Pulp.
                
        # Create the outer content frames
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Create self.menubar
        self.menubar = Menu(self.root)

        # Create the selection window
        self.selection_window = ttk.Frame(self.root, padding=(5, 5, 12, 12), borderwidth = 2, relief = 'solid') #shows list of ingredients and other possible restrictions

        # Create the ingredient selection window
        self.ingredient_selection_window = ttk.Frame(self.selection_window, padding=(5, 5, 5, 5)) # shows list of ingredients
        select_ing_label = Label(self.ingredient_selection_window, text='Select ingredients', font = ('Helvetica',10))  # Heading

        # Create the other selection window
        self.other_selection_window = ttk.Frame(self.selection_window, padding=(5, 5, 5, 5)) # shows list of other restrictions
        select_other_label = Label(self.other_selection_window, text='Select other restrictions', font = ('Helvetica',10))  # Heading
            
        # Create the main window for entering and displaying restrictions
        main_frame = ttk.Frame(self.root, padding=(5, 5, 12, 0))
        main_frame['borderwidth'] = 2
        main_frame['relief'] = 'solid'

        self.recipe_name_frame = ttk.Frame(main_frame, padding=(5, 5, 12, 12)) # window for displaying the current recipe's name
        restriction_frame = ttk.Frame(main_frame, padding=(5, 5, 12, 12)) # window for entering restrictions
        self.restriction_sf = VerticalScrolledFrame(restriction_frame)
        self.restriction_sf.frame_height = 500
        Label(master=self.restriction_sf.interior).grid(row=9000) # A hack to make sure that when a new 'other restriction' is added,
                                                              # you don't have to scroll down to see it.
        calc_frame = ttk.Frame(main_frame, padding=(15, 5, 10, 5))      # window holding the Calc button
        message_frame = ttk.Frame(main_frame, padding=(15, 5, 10, 5))   # window displaying messages. At the moment, this isn't used

        proj_frame = ttk.Frame(self.root, padding=(15, 5, 10, 5))            # window holding canvas displaying the 2-d projection

        proj_heading = ttk.Frame(proj_frame, padding=(5, 5, 5, 15))
        variable_info = ttk.Frame(proj_frame)
        self.proj_canvas = Canvas(proj_frame, width=450, height=450, bg='white', borderwidth=1, relief='solid')

        self.x_lab = Label(variable_info, text='x variable: Click right restriction name to select')
        self.y_lab = Label(variable_info, text='y variable: Click left restriction name to select')

        option_menu = Menu(self.menubar, tearoff=0)                 # create a pulldown menu, and add it to the menu bar

        self.vsf = VerticalScrolledFrame(self.ingredient_selection_window)
        self.vsf.frame_height = 400

        # GRID REMAINING WIDGETS

        # grid selection window
        self.selection_window.pack(side='left',fill=Y)
        self.ingredient_selection_window.grid(column = 0, row = 1, sticky = 'n')
        self.other_selection_window.grid(column = 0, row = 2, sticky = 'n')

        # grid the selection labels
        for label in [select_ing_label, select_other_label]:
            label.grid(column=0, row=0, columnspan=2)

        # grid the vertical scrolled frame containing the ingredients
        self.vsf.grid()

        # grid main frame
        main_frame.pack(side='left', fill='y')
        self.recipe_name_frame.grid(row = 0)
        restriction_frame.grid(row = 10)
        self.restriction_sf.pack()

        # grid recipe name
        self.recipe_name = StringVar()
        Entry(self.recipe_name_frame, textvariable=self.recipe_name, font=("Helvetica 12 italic")).grid()  # displays the name of the current recipe

     
        # grid oxide part of restriction frame
        oxide_heading_frame = ttk.Frame(self.restriction_sf.interior)
        oxide_heading_frame.grid(row=0, column=0, columnspan=7)
        Label(oxide_heading_frame, text='Oxides', font=('Helvetica', 12)).grid(column=0, row=0, columnspan=3)

        # grid ingredient part of restriction frame
        ingredient_heading_frame = ttk.Frame(self.restriction_sf.interior)
        ingredient_heading_frame.grid(row = 100, column = 0, columnspan = 7)
        Label(ingredient_heading_frame, text = 'Ingredients', font = ('Helvetica', 12)).grid()

        # grid other part of restriction frame
        other_heading_frame = ttk.Frame(self.restriction_sf.interior)
        other_heading_frame.grid(row = 1000, column = 0, columnspan = 7)
        Label(other_heading_frame, text = 'Other', font = ('Helvetica', 12)).grid()

        # grid calc frame
        calc_frame.grid(row = 1)

        # grid message frame. At the moment, this isn't used
        message_frame.grid(row = 3)

        # grid 2d projection frame
        proj_frame.pack(side='right', fill='y') #grid(column = 1, row = 1, rowspan=1000, sticky = 'nw')
        proj_heading.grid(row=0)
        Label(proj_heading, text='2-dimensional projection', font = ('Helvetica', 12)).grid()
        variable_info.grid(row=1, sticky=W)
        self.proj_canvas.grid(row=2)
        self.x_lab.grid(row=0, sticky=W)
        self.y_lab.grid(row=1, sticky=W)

            # SECTION 6
        # Create menus
        self.file_menu = Menu(self.menubar, tearoff=0)    
        self.file_menu.add_command(label="Recipes", command=open_recipe_menu)
        self.file_menu.add_command(label="Save as new recipe", command=save_new_recipe)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        option_menu.add_command(label="Edit Oxides", command=edit_oxides)
        option_menu.add_command(label="Edit Ingredients",
                                command=lambda : ing_dat.open_ingredient_editor(current_recipe, recipe_dict,
                                                                                self.ingredient_select_button, toggle_ingredient, update_var, self.entry_type))
        option_menu.add_command(label="Edit Other Restrictions", command=edit_other_restrictions)
        option_menu.add_command(label="Restriction Settings", command=restriction_settings)
        self.menubar.add_cascade(label="Options", menu=option_menu)
        self.root.config(menu=self.menubar)

        # Create and grid the percent/unity radio buttons:
        self.entry_type = StringVar()  # Make this an observable
        
        self.unity_radio_button = Radiobutton(oxide_heading_frame, text="UMF", variable=self.entry_type, value='umf_')
                                         #command=partial(update_oxide_entry_type, current_recipe, 'umf_'))
        self.unity_radio_button.grid(column=0, row=1)

        self.percent_wt_radio_button = Radiobutton(oxide_heading_frame, text="% weight", variable=self.entry_type, value='mass_perc_')
                                              #command=partial(update_oxide_entry_type, current_recipe, 'mass_perc_'))
        self.percent_wt_radio_button.grid(column=1, row=1)

        self.percent_mol_radio_button = Radiobutton(oxide_heading_frame, text="% mol", variable=self.entry_type, value='mole_perc_')
                                               #command=partial(update_oxide_entry_type, current_recipe, 'mole_perc_'))
        self.percent_mol_radio_button.grid(column=2, row=1)

        self.unity_radio_button.select()

        # Create and grid calc button:
        self.calc_button = ttk.Button(main_frame, text='Calculate restrictions')
        self.calc_button.grid()

        self.ingredient_select_button = {}

        # Move the following section to the model
        order_shelf_path = dirname(dirname(abspath(getsourcefile(lambda:0))))+'/model/persistent_data/OrderShelf'    ## There's probably a more elegant way of doing this
        with shelve.open(order_shelf_path) as order_shelf:
            self.ingredient_order = order_shelf['ingredients']
    ##        #oxide_order = ...
    ##        #other_order = ...

    ##    # Grid the message frame.  At the moment, this isn't used.
    ##    message_frame.grid(row = 3)

        self.other_select_button = {}

class DisplayRestriction:
    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, LOI, cost, etc'
    
    def __init__(self, display_frame, x_lab, y_lab, index, name, default_low, default_upp): #, objective_func, normalization, dec_pt=1):

        self.display_frame = display_frame   # Controller.mw.restriction_sf.interior
        self.x_lab = x_lab     # Controller.mw.x_lab
        self.y_lab = y_lab     # Controller.mw.y_lab
        self.index = index     # We will always have restr_dict[index] = DisplayRestriction(... , index, ...)
        self.name = name
        #self.objective_func = objective_func  # remove?
        #self.normalization = normalization    # remove?
        self.default_low = default_low        # remove??
        self.default_upp = default_upp        # remove??
        #self.dec_pt = dec_pt                  # remove?
        
        self.calc_bounds = {}   

        self.left_label_text = tk.StringVar()
        self.left_label_text.set('  '+prettify(self.name)+' : ')
        self.left_label = tk.Label(self.display_frame, textvariable=self.left_label_text)
        
        self.low = tk.DoubleVar()
        self.lower_bound = tk.Entry(self.display_frame, textvariable=self.low, width=5, fg='blue') #user lower bound
        self.low.set(self.default_low)

        self.upp = tk.DoubleVar()
        self.upper_bound = tk.Entry(self.display_frame, textvariable=self.upp, width=5, fg='blue') #user upper bound
        self.upp.set(self.default_upp)

        for eps in ['lower', 'upper']:
            self.calc_bounds[eps] = tk.Label(self.display_frame, bg='white', fg='red', width=5) #calculated lower and upper bounds
            self.calc_bounds[eps].config(text=' ')

        self.right_label_text = tk.StringVar()
        self.right_label_text.set(' : '+prettify(self.name)+'   ')
        self.right_label = tk.Label(self.display_frame, textvariable=self.right_label_text)

    def select(self, t):
        if t == 'x':
            self.left_label_text.set('* '+prettify(self.name)+' : ')
            self.x_lab.config(text='x variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+' *')
            self.y_lab.config(text='y variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
        else:
            print('Something\'s wrong')

    def deselect(self, t):
        if t == 'x':
            self.left_label_text.set('  '+prettify(self.name)+' : ')
            self.x_lab.config(text='x variable: Click right restriction name to select')
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+'  ')
            self.y_lab.config(text='y variable: Click left restriction name to select')
        else:
            print('Something\'s wrong')
                    
    def display(self, line):

        self.left_label.grid(row=line, column=0, sticky=tk.E)        # grid left restriction name
        
        self.lower_bound.grid(row=line, column=1)                 # grid lower bound entry box      
        self.upper_bound.grid(row=line, column=2)                 # grid upper bound entry box
    
        self.calc_bounds['lower'].grid(row=line, column=4)             # grid calculated lower bound box
        self.calc_bounds['upper'].grid(row=line, column=5)             # grid calculated upper bound box

        self.right_label.grid(row=line, column=6, sticky=tk.W)       # grid right restriction name

    def remove(self, recipe):     # remove recipe from this?
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
                       self.right_label]:
            widget.grid_forget()    # remove widgets corresponding to that restriction
        self.low.set(self.default_low)
        self.upp.set(self.default_upp)
        for eps in ['lower', 'upper']:
            self.calc_bounds[eps].config(text='')
        v = dict(recipe.variables)
        for t in v:
            if self.index == v[t]:
                self.deselect(t)
                del recipe.variables[t]

    def hide(self):  # to be used with oxide options
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
                       self.right_label]:
            widget.grid_forget()

    def display_calc_bounds(self, calc_value):  # Do we use this?
        for eps in ['lower', 'upper']:
            self.calc_bounds[eps].config(text=('%.' + str(self.dec_pt) + 'f') % self.calc_value[eps])
