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

k = 20  # number of sample points to take in the case where the denominators are different
solver = GLPK()
#solver = PULP_CBC_CMD()

def two_dim_projection(self, var0, var1, var2, var3):   # Calculates a set of vertices in R^2 whose convex hull is
                                            # the projection of the linear programming problem, self, onto a 2d subspace
    # Start by finding two distinct points on the 2 dimensional projection of the feasible reason. This assumes
    # the region is bounded.

    self.constraints['normalization'] = eval(var2) == 1

    initial_vertices = []
    for eps in [-1, 1]:
        self += eps * var0
        self.solve(solver)
        initial_vertices.append([pulp.value(var0), pulp.value(var1)]) 
    
    if var2 == var3:

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
                    return   # Change this
                
                v = [v1[0] - v0[0], v1[1] - v0[1]]
                d = abs(v[0]) + abs(v[1]) + 1
                #print(d)
                s = - v[1]/d*var0 + v[0]/d*var1
                self += s
                self.solve(solver)
                v2 = [pulp.value(var0), pulp.value(var1)]

                #print(pulp.value(self.objective))
                #print('Difference = : '+str(pulp.value(self.objective) + (v[1]*v0[0] - v[0]*v0[1])/d))
                if abs(pulp.value(self.objective) + (v[1]*v0[0] - v[0]*v0[1])/d) < 0.1**5:   # Look into what error bounds PuLP uses
                    vertices_pre.remove(v0)                     
                    vertices_post.append(v0)                 
                else:
                    vertices_pre.insert(1,v2)

            if count==100:
                print('Error: count overflowed')
           
            initial_vertices.reverse()  # After the 'top' part of the for loop, we switch the order of the vertices to get ready for the 'bottom' part

        #print(vertices_post)
        return vertices_post
    
    else:
        a = initial_vertices[0][0]
        b = initial_vertices[1][0]
 

        width = b - a - 0.0002
        d = width / k
        vertices = {-1:[], 1:[]}

        for i in range(k + 1):
            x = 0.0001 + a + d * i
            self.constraints['normalization'] = eval(var3) == 1
            self.constraints['fix_x'] = var0 == x * eval(var2)
            for eps in [-1,1]:
                self += eps * var1
                #print(self.constraints)
                self.solve()
                vertices[eps].append([x, eps * pulp.value(self.objective)])
        del self.constraints['fix_x']    # Not sure if this is necessary
        vertices[-1].reverse()
        #print(vertices[1] + vertices[-1])
        return vertices[1] + vertices[-1]

LpProblem.two_dim_projection = two_dim_projection  # Add the method two_dim_projection to the predefined LpProblem class.


            
