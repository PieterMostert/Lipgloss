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

# Initialize oxides:
oxides = ('SiO2', 'Al2O3', 'B2O3', 'MgO', 'CaO', 'SrO', 'BaO', 'ZnO', 'Li2O', 'Na2O', 'K2O', 'P2O5',
          'Fe2O3', 'TiO2', 'MnO2')

molar_masses = (60.083, 101.961, 69.617, 40.304, 56.077, 103.619, 153.329, 81.379, 29.879, 61.979, 94.191,
                141.943, 159.687, 79.865, 86.937) 
molar_mass_dict = {oxides[i]: molar_masses[i] for i in range(len(oxides))}

fluxes = ('Li2O', 'Na2O', 'MgO', 'K2O', 'CaO', 'ZnO', 'SrO', 'BaO') 
