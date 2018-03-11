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

# Construct prettify function
pretty_dict = {'SiO2':'SiO\u2082',
               'Al2O3':'Al\u2082O\u2083',
               'B2O3':'B\u2082O\u2083',
               'Li2O':'Li\u2082O',
               'Na2O':'Na\u2082O',
               'K2O':'K\u2082O',
               'P2O5':'P\u2082O\u2085',
               'Fe2O3':'Fe\u2082O\u2083',
               'TiO2':'TiO\u2082',
               'MnO2':'MnO\u2082',
               'SiO2_Al2O3':'SiO\u2082 : Al\u2082O\u2083',
               'cost':'Cost',
               'mass_perc_':'% weight',
               'mole_perc_':'% mole'}

def prettify(text):
    try:
        return pretty_dict[text]
    except:
        return text

def pretty_entry_type(text):
    if text == 'um':
        return ' UMF'
    elif text == 'ma':
        return ' % weight'
    elif text == 'mo':
        return ' % mole'
    else:
        return ''
