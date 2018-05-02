from tkinter import *
from functools import partial   

# For the drag manager to work, the row numbers (i.e. widget.grid_info()['row']) must be consecutive integers, starting from 0.
# This means if we delete a row, the rows below must have their row numbers decreased by 1.

class DragManager():
    def __init__(self, reorder_func):
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
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)    # Widget whose position will be taken over by dragged widget.
        
        try:
            yr = target.grid_info()['row']             # Row you want to drag the widget to.  
            self.reorder_func(y0, yr)
        except:
            pass
