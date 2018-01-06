import numpy as np


class Poly(object):
    def __init__(self, points):
        self.points = points

    def move(self, x, y):
        """return a new polygon moved by x, y"""
        return Poly([(x + p_x, y + p_y) for (p_x, p_y) in self.points])


    def collidepoly(self, polygon):
        '''
        Return True and the MPV if the shapes collide. Otherwise, return False and
        None.

        p1 and p2 are lists of ordered pairs, the vertices of the polygons in the
        counterclockwise direction.
        '''

        #p1 = [np.array(v, 'float64') for v in p1]
        #p2 = [np.array(v, 'float64') for v in p2]
        p1 = [np.array(v, 'float64') for v in self.points]
        p2 = [np.array(v, 'float64') for v in polygon.points]

        edges = self.edges_of(p1)
        edges += self.edges_of(p2)
        orthogonals = [self.orthogonal(e) for e in edges]

        push_vectors = []
        for o in orthogonals:
            separates, pv = self.is_separating_axis(o, p1, p2)

            if separates:
                # they do not collide and there is no push vector
                return False, None
            else:
                push_vectors.append(pv)

        # they do collide and the push_vector with the smallest length is the MPV
        mpv =  min(push_vectors, key=(lambda v: np.dot(v, v)))

        # assert mpv pushes p1 away from p2
        d = self.centers_displacement(p1, p2) # direction from p1 to p2
        if np.dot(d, mpv) > 0: # if it's the same direction, then invert
            mpv = -mpv

        return True, mpv


    def centers_displacement(self, p1, p2):
        """
        Return the displacement between the geometric center of p1 and p2.
        """
        # geometric center
        c1 = np.mean(np.array(p1), axis=0)
        c2 = np.mean(np.array(p2), axis=0)
        return c2 - c1

    def edges_of(self, vertices):
        """
        Return the vectors for the edges of the polygon p.

        p is a polygon.
        """
        edges = []
        N = len(vertices)

        for i in range(N):
            edge = vertices[(i + 1)%N] - vertices[i]
            edges.append(edge)

        return edges

    def orthogonal(self, v):
        """
        Return a 90 degree clockwise rotation of the vector v.
        """
        return np.array([-v[1], v[0]])


    def is_separating_axis(self, o, p1, p2):
        """
        Return True and the push vector if o is a separating axis of p1 and p2.
        Otherwise, return False and None.
        """
        min1, max1 = float('+inf'), float('-inf')
        min2, max2 = float('+inf'), float('-inf')

        for v in p1:
            projection = np.dot(v, o)

            min1 = min(min1, projection)
            max1 = max(max1, projection)

        for v in p2:
            projection = np.dot(v, o)

            min2 = min(min2, projection)
            max2 = max(max2, projection)

        if max1 >= min2 and max2 >= min1:
            d = min(max2 - min1, max1 - min2)
            # push a bit more than needed so the shapes do not overlap in future
            # tests due to float precision
            d_over_o_squared = d/np.dot(o, o) + 1e-10
            pv = d_over_o_squared*o
            return False, pv
        else:
            return True, None


#poly1 = Poly([(0,0),(10,0),(0,5)])
#poly1 = Poly([(-0.5,-0.9),(9.5,-0.9),(-0.5,4.1)])
#poly2 = Poly([(4,2),(10,2),(6,6)])

#print(poly1.collidepoly(poly2))

#collision, mpv = poly1.collidepoly(poly2)

#print(mpv)
#poly1 = poly1.move(mpv[0], mpv[1])
#print(poly1.collidepoly(poly2))




#p1 = [(0,0),(10,0),(0,5)]
#p1 = [(-0.5,-0.9),(9.5,-0.9),(-0.5,4.1)]
#p2 = [(4,2),(10,2),(6,6)]



#a = collide(p1, p2)
#print(a)