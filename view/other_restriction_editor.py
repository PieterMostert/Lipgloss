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

import tkinter.messagebox
from numbers import Number

from .dragmanager import *
from .main_window import MainWindow
from .vert_scrolled_frame import VerticalScrolledFrame
from .pretty_names import prettify

class DisplayOtherRestriction:
    """A class used to display the line corresponding to a restriction in the other restriction editor"""
    def __init__(self, index, core_data, frame):
        ot = core_data.other_dict[index]
        self.delete_button =  ttk.Button(master=frame, text='X', width=2)
        self.name_entry = Entry(master=frame, width=20)
        self.numerator_coefs_entry = Entry(master=frame, width=30)
        self.normalization_entry = Entry(master=frame, width=30)
        self.def_low_entry = Entry(master=frame, width=12)
        self.def_upp_entry = Entry(master=frame, width=12)
        self.dec_pt_entry = Entry(master=frame, width=10)
        self.name_entry.insert(0, ot.name)
        self.numerator_coefs_entry.insert(0, ot.numerator_coefs)
        self.normalization_entry.insert(0, ot.normalization)
        self.def_low_entry.insert(0, ot.def_low)
        self.def_upp_entry.insert(0, ot.def_upp)
        self.dec_pt_entry.insert(0, ot.dec_pt)

    def display(self, pos, order):
        self.delete_button.grid(row=pos, column=0)
        self.name_entry.grid(row=pos, column=1, padx=3, pady=3)
        self.numerator_coefs_entry.grid(row=pos, column=2, padx=3, pady=3)
        self.normalization_entry.grid(row=pos, column=3, padx=3, pady=3)
        self.def_low_entry.grid(row=pos, column=4, padx=3, pady=3)
        self.def_upp_entry.grid(row=pos, column=5, padx=3, pady=3)
        self.dec_pt_entry.grid(row=pos, column=6, padx=3, pady=3)

    def delete(self):
        for widget in [self.delete_button, self.name_entry, self.numerator_coefs_entry, self.normalization_entry, \
                       self.def_low_entry, self.def_upp_entry, self.dec_pt_entry]:
            widget.destroy()

class OtherRestrictionEditor(MainWindow):
    """Window that lets users enter / delete other restrictions, and rearrange the order in which they are displayed"""

    def __init__(self, core_data, order, reorder_other_restrictions):
        self.toplevel = Toplevel()
        self.toplevel.title("Other Restriction Editor")

        self.other_restriction_editor_headings = Frame(self.toplevel)
        self.other_restriction_editor_headings.pack()
        self.i_e_scrollframe = VerticalScrolledFrame(self.toplevel)
        self.i_e_scrollframe.frame_height = 200
        self.i_e_scrollframe.pack()
        other_restriction_editor_buttons = Frame(self.toplevel)
        other_restriction_editor_buttons.pack()

        # Place the headings on the other_restriction_editor. There is some not-entirely-successful fiddling involved to try
        # to get the headings to match up with their respective columns:
        Label(master=self.other_restriction_editor_headings, text='', width=5).grid(row=0, column=0)  # Blank label above the delete buttons
        Label(master=self.other_restriction_editor_headings, text='', width=5).grid(row=0, column=1)  # Blank label above the delete buttons
        Label(master=self.other_restriction_editor_headings, text='    Restriction Name', width=20).grid(row=0, column=2)
        Label(master=self.other_restriction_editor_headings, text='Numerator Coefficients', width=30).grid(row=0, column=3)
        Label(master=self.other_restriction_editor_headings, text='Normalization', width=20).grid(row=0, column=4)
        Label(master=self.other_restriction_editor_headings, text='Def lower bnd', width=12).grid(row=0, column=5)
        Label(master=self.other_restriction_editor_headings, text='Def upper bnd', width=12).grid(row=0, column=6)
        Label(master=self.other_restriction_editor_headings, text='Dec places', width=10).grid(row=0, column=7)
        Label(master=self.other_restriction_editor_headings, text='', width=5).grid(row=0, column=8)  # Blank label above the scrollbar
        Label(master=self.other_restriction_editor_headings, text='', width=5).grid(row=0, column=9)  # Blank label above the scrollbar

        # Create drag manager for restriction rows:
        self.ing_dnd = DragManager(reorder_other_restrictions)
        
        # Create and display the rows:
        self.display_other_restrictions = {}
        for r, i in enumerate(order["other"]):
            self.display_other_restrictions[i] = DisplayOtherRestriction(i, core_data, self.i_e_scrollframe.interior)
            self.display_other_restrictions[i].display(r, order)    
            self.ing_dnd.add_dragable(self.display_other_restrictions[i].name_entry)    # This lets you drag the row corresponding to a restriction by right-clicking on its name   
                
        # This label is hack to make sure that when a new other restriction is added, you don't have to scroll down to see it:
        Label(master=self.i_e_scrollframe.interior).grid(row=9000) 

        self.new_other_restr_button = ttk.Button(other_restriction_editor_buttons, text='New restriction', width=20)
        self.new_other_restr_button.pack(side='left')   
        self.update_button = ttk.Button(other_restriction_editor_buttons, text='Update', width=20)
        self.update_button.pack(side='right')

        self.i_e_scrollframe.interior.focus_force()

    def new_other_restriction(self, i, core_data, order):
        self.display_other_restrictions[i] = DisplayOtherRestriction(i, core_data, self.i_e_scrollframe.interior) 
        self.display_other_restrictions[i].display(int(i), order)
        self.ing_dnd.add_dragable(self.display_other_restrictions[i].name_entry)

