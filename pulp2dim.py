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

from pulp import *

def two_dim_projection(self, var0, var1):   # Calculates a set of vertices in R^2 whose convex hull is
                                            # the projection of the linear programming problem, self, onto a 2d subspace
    # Start by finding two distinct points on the 2 dimensional projection of the feasible reason. This assumes
    # the region is bounded.
    initial_x_coords = []
    for eps in [-1,1]:
        self += eps*var0
        #self.solve()
        self.solve(GLPK())
        initial_x_coords.append(eps*pulp.value(self.objective))
    
    initial_vertices = []
    for x in initial_x_coords:
            
        self += var0 == x, 'x'
        self += var1
        #self.solve()
        self.solve(GLPK())
        initial_vertices.append([x, pulp.value(self.objective)])  

        del self.constraints['x']

    # Find remaining points:
    vertices_post = []
    
    for edge in ['top', 'bottom']:
        vertices_pre = []
        vertices_pre += initial_vertices
        
        count = 0    # delete once sure the algorithm always terminates
        
        while len(vertices_pre) > 1 and count <100:
            count += 1
            v0 = vertices_pre[0]
            v1 = vertices_pre[1]

            if v0 == v1:
                print('points coincide')
                return
            
            v = [v1[0] - v0[0], v1[1] - v0[1]]   #vector subtraction. Why are there no built in vectors in Python?
            s = - v[1]*var0 + v[0]*var1
            self += s
            #self.solve()
            self.solve(GLPK())
            v2 = [pulp.value(var0), pulp.value(var1)]
            
            if abs(pulp.value(self.objective) + v[1]*v0[0] - v[0]*v0[1]) < 0.1**5:   #Look into what error bounds PuLP uses
                vertices_pre.remove(v0)                     
                vertices_post.append(v0)                 
            else:
                vertices_pre.insert(1,v2)
       
        initial_vertices.reverse()  # After the 'top' part of the for loop, we switch the order of the vertices to get ready for the 'bottom' part
    
    return vertices_post

LpProblem.two_dim_projection = two_dim_projection


            
