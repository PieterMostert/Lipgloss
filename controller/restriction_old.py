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
import sys
from os.path import abspath, dirname
from inspect import getsourcefile
sys.path.append(dirname(dirname(abspath(getsourcefile(lambda:0))))+'\model') # allows us to treat lipgloss like a built in package

from lipgloss.core_data import OxideData, CoreData, Oxide, Ingredient
from lipgloss.lp_recipe_problem import LpRecipeProblem
from lipgloss.recipes import Recipe, restr_keys
from lipgloss.restrictions import Restriction

import model.serializers.recipeserializer
from model.model import Model
#from model.restrictions import Restriction

from view.main_window import MainWindow, DisplayRestriction, RecipeMenu
from view.pretty_names import prettify, pretty_entry_type

import pulp
import tkinter as tk
from tkinter import ttk
from functools import partial
import shelve
import copy

##class Restriction:
##    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, LOI, cost, etc'
##    display_frame = None   # Will be assigned later to be Controller.mw.restriction_sf.interior
##    x_lab = None   # Will be assigned later to be Controller.mw.x_lab
##    y_lab = None   # Will be assigned later to be Controller.mw.y_lab
##    
##    def __init__(self, index, name, objective_func, normalization, default_low, default_upp, dec_pt=1):
##
##        self.index = index     # We will always have restr_dict[index] = Restriction(frame, index, ...)
##        self.name = name
##        self.objective_func = objective_func
##        self.normalization = normalization
##        self.default_low = default_low
##        self.default_upp = default_upp
##        self.dec_pt = dec_pt
##        
##        self.calc_bounds = {}   
##
##        self.left_label_text = tk.StringVar()
##        self.left_label_text.set('  '+prettify(self.name)+' : ')
##        self.left_label = tk.Label(self.display_frame, textvariable=self.left_label_text)
##        
##        self.low = tk.DoubleVar()
##        self.lower_bound = tk.Entry(self.display_frame, textvariable=self.low, width=5, fg='blue') #user lower bound
##        self.low.set(self.default_low)
##
##        self.upp = tk.DoubleVar()
##        self.upper_bound = tk.Entry(self.display_frame, textvariable=self.upp, width=5, fg='blue') #user upper bound
##        self.upp.set(self.default_upp)
##
##        for eps in ['lower', 'upper']:
##            self.calc_bounds[eps] = tk.Label(self.display_frame, bg='white', fg='red', width=5) #calculated lower and upper bounds
##            self.calc_bounds[eps].config(text=' ')
##
##        self.right_label_text = tk.StringVar()
##        self.right_label_text.set(' : '+prettify(self.name)+'   ')
##        self.right_label = tk.Label(self.display_frame, textvariable=self.right_label_text)
##
##    def select(self, t):
##        if t == 'x':
##            self.left_label_text.set('* '+prettify(self.name)+' : ')
##            self.x_lab.config(text='x variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
##        elif t == 'y':
##            self.right_label_text.set(' : '+prettify(self.name)+' *')
##            self.y_lab.config(text='y variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
##        else:
##            print('Something\'s wrong')
##
##    def deselect(self, t):
##        if t == 'x':
##            self.left_label_text.set('  '+prettify(self.name)+' : ')
##            self.x_lab.config(text='x variable: Click right restriction name to select')
##        elif t == 'y':
##            self.right_label_text.set(' : '+prettify(self.name)+'  ')
##            self.y_lab.config(text='y variable: Click left restriction name to select')
##        else:
##            print('Something\'s wrong')
##                    
##    def display(self, line):
##
##        self.left_label.grid(row=line, column=0, sticky=tk.E)        # grid left restriction name
##        
##        self.lower_bound.grid(row=line, column=1)                 # grid lower bound entry box      
##        self.upper_bound.grid(row=line, column=2)                 # grid upper bound entry box
##    
##        self.calc_bounds['lower'].grid(row=line, column=4)             # grid calculated lower bound box
##        self.calc_bounds['upper'].grid(row=line, column=5)             # grid calculated upper bound box
##
##        self.right_label.grid(row=line, column=6, sticky=tk.W)       # grid right restriction name
##
##    def remove(self, recipe):
##        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
##                       self.right_label]:
##            widget.grid_forget()    # remove widgets corresponding to that restriction
##        self.low.set(self.default_low)
##        self.upp.set(self.default_upp)
##        for eps in ['lower', 'upper']:
##            self.calc_bounds[eps].config(text='')
##        v = dict(recipe.variables)
##        for t in v:
##            if self.index == v[t]:
##                self.deselect(t)
##                del recipe.variables[t]
##
##    def hide(self):  # to be used with oxide options
##        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
##                       self.right_label]:
##            widget.grid_forget()
##
##    def display_calc_bounds(self, calc_value):
##        for eps in [-1, 1]:
##            self.calc_bounds[eps].config(text=('%.' + str(self.dec_pt) + 'f') % self.calc_value[eps])
