# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:04:28 2016

@author: Sam
"""


class Graph(object):
    def __init__(self, vertices=[], edges=[], add_vertices_from_edges=True, 
                 do_validate_edges=True, serre=False):
        """Initialises an unlabelled oriented graph object"""
        self.vertices = vertices
        self.edges = edges
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

def CompleteGraph(n):
    return Graph([],[[i,j] for i in range(1,n+1) for j in range(1,n+1) if i < j])
         
    