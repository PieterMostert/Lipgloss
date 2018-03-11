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

from model.core_data import CoreData
from view.main_window import MainWindow
from model.restrictions import Restriction
from model.lp_recipe_problem import LpRecipeProblem
import pulp
from model.recipes import Recipe


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myMoney.addCallback(self.MoneyChanged)
        self.view1 = MainWindow(root)
        #self.view2 = ChangerWidget(self.view1)
        self.view1..config(command=self.AddMoney)
        self.view2.removeButton.config(command=self.RemoveMoney)
        self.MoneyChanged(self.model.myMoney.get())
        
##    def AddMoney(self):
##        self.model.addMoney(10)
##
##    def RemoveMoney(self):
##        self.model.removeMoney(10)
##
##    def MoneyChanged(self, money):
##        self.view1.SetMoney(money)
