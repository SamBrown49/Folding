# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:04:28 2016

@author: Sam

Defines a class for a graph, and some basic graphs.

"""
class Vertex(object):
    def __init__(self, id):
        self.id = id
        
class Edge(object):
    def __init__(self, initial, terminal, id):
        self.initial = initial
        self.terminal  = terminal
        self.id = id
        
    def __str__(self):
        return "[%s, %s]" % (self.initial, self.terminal)


class Graph(object):
    def __init__(self, 
                 vertices=[], edges=[], add_vertices_from_edges=True, 
                 do_validate_edges=True, serre=False):
        """Initialises an unlabelled oriented graph object"""
        #self.vertices = vertices
        self.vertices = [Vertex(vertex) for vertex in vertices]
        self.edges = [Edge(edge[0], edge[1], ) for edge in edges]
        self.add_vertices_from_edges = add_vertices_from_edges
        self.do_validate_edges = do_validate_edges
        self.serre = serre
        if self.add_vertices_from_edges:
            for edge in self.edges:
                for vertex in edge:
                    if vertex not in self.vertices:
                        self.vertices.append(vertex)
                        print "Added vertex %s" % vertex
        if self.do_validate_edges:
            self.validate_edges(True)
        if self.serre:
            reversed_edges = [[j,i] for [i,j] in self.edges]
            self.edges.extend(reversed_edges)
            self.good_edges = [Edge(edge[0], edge[1]) for edge in self.edges]
    
    def edges(self):
        print self.edges
    
    def show(self):
        print "Vertices: %s" % self.vertices
        print "Edges: %s" % self.edges
            

    def validate_edges(self, add_loops_for_singletons=True):
        """Converts edges given as paths into individual edges"""
        real_edges = []
        for edge in self.edges:
            if len(edge) == 2:
                real_edges.append(edge)
            elif len(edge) > 2:
                for i in range(len(edge)-1):
                    real_edges.append([edge[i], edge[i+1]])
            elif len(edge) == 1:
                if add_loops_for_singletons:
                    real_edges.append([edge[0], edge[0]])
        self.edges = real_edges
        self.good_edges = [Edge(edge[0], edge[1]) for edge in self.edges]
        
    def edge_multiplicity(self, edge):
        """
        Returns the multiplicity of a particular edge [v,w] in the graph
        [v,w] is not considered to be the same edge as [w,v]
        """
        return self.edges.count(edge)

    def neighbouring_edges(self, vertex, orientation=None):
        """Returns a list of edges containing a given vertex"""
        if orientation == None:
            return [edge for edge in self.edges if vertex in edge]
        elif orientation == "outward":
            return [edge for edge in self.edges if vertex==edge[0]]
        elif orientation == "inward":
            return [edge for edge in self.edges if vertex==edge[1]]
        else:
            print "Error! Argument must be inward or outward."
            return None

    def neighbours(self, vertex):
        """Returns the neighbours of a given vertex"""
        if vertex not in self.vertices:
            print "Error: vertex not found!"
            return False
        else:
            neighbours = [edge[1-edge.index(vertex)] for edge in self.edges if vertex in edge]
            return neighbours

    def graph_dict(self):
        """Returns the graph as a dictionary of the form
        {vertex:[neigbours], ...}"""
        dcty = {}
        for vertex in self.vertices:
            dcty[vertex] = self.neighbours(vertex)
        return dcty

    def spanning_tree(self):
        """Returns a spanning tree of the graph"""
        spanning_tree_edges = []
        spanning_tree_vertices = [self.vertices[0]]
        vertices_to_check = [self.vertices[0]]
        while len(spanning_tree_vertices) < len(self.vertices):
            for vertex in vertices_to_check:
                for edge in self.neighbouring_edges(vertex):
                    neighbour = edge[1-edge.index(vertex)]
                    if neighbour not in spanning_tree_vertices:
                        spanning_tree_edges.append(edge)
                        spanning_tree_vertices.append(neighbour)
                        vertices_to_check.append(neighbour)
#                        print vertices_to_check
                vertices_to_check.remove(vertex)
        return Graph(spanning_tree_vertices, spanning_tree_edges)

    def rank(self):
        """Computes the rank of the graph using a spanning tree"""
        return len(self.edges) - len(self.spanning_tree().edges)
        
    def mapto(self, map_dict={}, image=True):
        if map_dict.keys() != self.vertices:
            print "Error: wrong input vertices."
            map_dict = input("Please enter a new map in the form {v:f(v)}")
        return map_dict
        
    def validate_homomorphism(self, map, image=None):
        """Checks that a dictionary defines a graph homomorphism"""
        if image==None:
            print "No image graph provided."
            for vertex in self.vertices:
                if vertex in map.keys:
                    print "Checked vertex %s" % vertex
                else:
                    print "Map not defined on vertex %s" % vertex
                    return False
                return True
        else:
            print "Image graph: "
            image.show()
            print "Map: %s" % map
            for edge in self.edges:
                mapped_edge = [map[edge[0]], map[edge[1]]]
                print "Checking edge: %s. Image should be: %s" % (edge, mapped_edge)      
                if mapped_edge in image.edges:
                    pass
                else:
                    print "Fails to be homomorphism: %s not in the image graph." % mapped_edge
                    return False
            return True
    

def CompleteGraph(n):
    return Graph(range(1,n+1),[[i,j] for i in range(1,n+1) for j in range(1,n+1) if i < j])
    
def Bouquet(n):
    return Graph([1], [[1,1]]*n)
    
def Cycle(n):
    return Graph(range(1,n+1), [[i,i+1] for i in range(1,n)] + [[n,1]])
         
    