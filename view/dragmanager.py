from tkinter import *
import tkinter
#import copy
import shelve
from functools import partial

def update_shelf(name, dictionary):
    with shelve.open(name) as shelf:
        for item in shelf:
            del shelf[item]
        shelf.update(dictionary)    

# For the drag manager to work, the row numbers (i.e. widget.grid_info()['row']) must be consecutive integers, starting from 0.
# This means if we delete a row, the rows below must have their row numbers decreased by 1.

class DragManager():
    def __init__(self, family_dict, order_shelf, family_name, grid_func, reorder_func):
        self.family_dict = family_dict  # Dictionary whose values are those objects whose order is being changed
        self.order_shelf = order_shelf  # Shelf that keeps track of the orders of difference families of objects.
                                        # order_shelf[family_name] is a list of indices in the order they will be displayed
        self.family_name = family_name  # Text string denoting the family in question.
        self.grid_func = grid_func      # Function that grids widgets associated to members of the family.
                                        # To be more specific, grid_func(family_dict[j], i) grids family_dict[j] in row i.
        self.reorder_func = reorder_func
        
    def add_dragable(self, widget):
        widget.bind("<ButtonPress-3>", partial(self.on_start, widget))    # Right-click
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-3>", partial(self.on_drop, widget))
        #widget.configure(cursor="hand1")

    def on_start(self, widget, event):
        # You could use this method to create a floating window
        # that represents what is being dragged.
        widget.configure(cursor="sb_v_double_arrow") 

    def on_drag(self, event):
        # You could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, widget, event):
        widget.configure(cursor="xterm")    # This is assuming the widget is an entry widget
        # Find the widget under the cursor:
        y0 = event.widget.grid_info()['row']           # Row of widget you're dragging.
        #print('y0 = '+str(y0))
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)    # Widget whose position will be taken over by dragged widget.
        
        try:
            yr = target.grid_info()['row']             # Row you want to drag the widget to.
            #print('yr = '+str(yr))
            
            with shelve.open(self.order_shelf) as order_shelf:
                temp_list = order_shelf[self.family_name]
                #print(temp_list)
                temp_list.insert(yr, temp_list.pop(y0))
                order_shelf[self.family_name] = temp_list
                

            #new_family_dict = {}
            for i, j in enumerate(temp_list):
                #print(j)
                self.grid_func(self.family_dict[j],i)
                #new_family_dict[j] = self.family_dict[j]

            #self.family_dict = new_family_dict
            #print('about to reorder')
            self.reorder_func(temp_list)   # This changes all the other stuff that needs to be changed.
        except:
            pass
        
##top = Tk()
##dnd = DragManager("ItemShelf", grid_func)
##with shelve.open("ItemShelf") as item_shelf:
##    item_shelf_copy = dict(item_shelf)
##    for i,item in enumerate(list(item_shelf)):
##        item_shelf_copy[item].create_label(top)
##        item_shelf_copy[item].widgets['label'].grid(row=i)
##        dnd.add_dragable(item_shelf_copy[item].widgets['label'])    

