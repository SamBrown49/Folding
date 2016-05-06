# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:04:28 2016

@author: Sam

Defines a class for a graph, and some basic graphs.

"""
class Vertex(object):
    def __init__(self, id=None):
        self.id = id
        
class Edge(object):
    def __init__(self, initial, terminal, id=None):
        self.initial = initial
        self.terminal  = terminal
        self.id = id
        return None
        
    def __str__(self):
        return "[%s, %s]" % (self.initial, self.terminal)
        
    def __name__(self):
        return self.id


class Graph(object):
    def __init__(self, 
                 vertices=[], edges=[], edge_labels=[], add_vertices_from_edges=True, 
                 do_validate_edges=True, add_loops_for_singletons = True, serre=False):
        """Initialises an unlabelled oriented graph object"""
        #self.vertices = vertices #Temporary list storing vertices before naming
        self.edges = edges #Temporary list storing edges before they are named
        self.add_vertices_from_edges = add_vertices_from_edges
        self.do_validate_edges = do_validate_edges
        self.serre = serre
        self.add_loops_for_singletons = add_loops_for_singletons
        if self.add_vertices_from_edges:
            for edge in self.edges:
                try:
                    for vertex in edge:
                        if vertex not in vertices:
                            vertices.append(vertex)
                            print "Added vertex %s" % vertex
                except TypeError:
                    raise AttributeError("Graph incorrectly defined: edges must be lists")
        if self.do_validate_edges:
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
        if self.serre:
            reversed_edges = [[j,i] for [i,j] in self.edges]
            self.edges.extend(reversed_edges)  
        self.vertexdict = {}
        for vertex in vertices:
            self.vertexdict[vertex] = Vertex(vertex)            
        #self.vertices = [Vertex(vertex) for vertex in vertices]
        self.edges = [Edge(self.vertexdict[edge[0]],
                           self.vertexdict[edge[1]],
                           "e_%d" % i) for i, edge in enumerate(self.edges)]
        self.last_edge_index = len(self.edges)
        
    def vertices(self):
        return self.vertexdict.values()
    
    def show_edges(self):
        for edge in self.edges:
            print edge.id, edge.initial.id, "-->", edge.terminal.id
            
    def show_vertices(self):
        for vertex in self.vertices():
            print vertex.id
    
    def show(self):
        print "Vertices: "        
        self.show_vertices()
        print ""
        print "Edges: "
        self.show_edges()
        
    def edge_multiplicity(self, initial, terminal):
        """
        Returns the multiplicity of a particular edge [v,w] in the graph
        [v,w] is not considered to be the same edge as [w,v]
        """
        count = 0
        multiple_edge_ids = []
        for edge in self.edges:
            if edge.initial.id == initial.id and edge.terminal.id == terminal.id:
                count +=1
                multiple_edge_ids.append(edge.id)
        print count, multiple_edge_ids
        return count, multiple_edge_ids
                           

    def neighbouring_edges(self, vertexid, orientation=None):
        """Returns a list of edges containing a given vertex"""
        if orientation == None:
            list_of_neighbouring_edges = [edge for edge in self.edges if 
            edge.initial.id == vertexid or edge.terminal.id == vertexid]
            for edge in list_of_neighbouring_edges:
                print edge.id, edge.initial.id, "-->", edge.terminal.id 
            return list_of_neighbouring_edges
        elif orientation == "outward":
            list_of_neighbouring_edges = [edge for edge in self.edges if 
            edge.initial.id == vertexid]
            for edge in list_of_neighbouring_edges:
                print edge.id, edge.initial.id, "-->", edge.terminal.id 
            return list_of_neighbouring_edges
        elif orientation == "inward":
            list_of_neighbouring_edges = [edge for edge in self.edges if 
            edge.terminal.id == vertexid]
            for edge in list_of_neighbouring_edges:
                print edge.id, edge.initial.id, "-->", edge.terminal.id 
            return list_of_neighbouring_edges
        else:
            raise AttributeError("Error! Argument must be inward or outward.")
            #print "Error! Argument must be inward or outward."

    def neighbours(self, vertexid):
        """Returns the neighbours of a given vertex"""
        if vertexid not in [v.id for v in self.vertices()]:
            print "Error: vertex not found!"
            return False
        else:
            neighbours=[]
            children = [edge.terminal for edge in self.edges if edge.initial.id == vertexid]
            parents = [edge.initial for edge in self.edges if edge.terminal.id == vertexid]
            neighbours.extend(children)
            neighbours.extend(parents)
            return neighbours

    def graph_dict(self):
        """Returns the graph as a dictionary of the form
        {vertex:[neigbours], ...}"""
        dcty = {}
        for vertex in self.vertices():
            dcty[vertex.id] = self.neighbours(vertex.id)
        return dcty

    def spanning_tree(self):
        """Returns a spanning tree of the graph"""
        spanning_tree_edges = []
        spanning_tree_vertices = [self.vertices()[0]]
        vertices_to_check = [self.vertices()[0]]
        while len(spanning_tree_vertices) < len(self.vertices()):
            for vertex in vertices_to_check:
                print vertex.id
                print "Neighbouring edges: ", self.neighbouring_edges(vertex.id)
                for edge in self.neighbouring_edges(vertex.id):
                    if edge.initial != vertex:
                        neighbour = edge.initial
                    if edge.terminal != vertex:
                        neighbour = edge.terminal
                    else:
                        pass
                    if neighbour not in spanning_tree_vertices:
                        spanning_tree_edges.append(edge)
                        spanning_tree_vertices.append(neighbour)
                        vertices_to_check.append(neighbour)
                        print "Vertices to check: ", [v.id for v in vertices_to_check]
                vertices_to_check.remove(vertex)
        return spanning_tree_vertices, spanning_tree_edges

    def rank(self):
        """Computes the rank of the graph using a spanning tree"""
        return len(self.edges) - len(self.spanning_tree().edges)
        
    def mapto(self, map_dict={}, image=True):
        if map_dict.keys() != self.vertices():
            print "Error: wrong input vertices."
            map_dict = input("Please enter a new map in the form {v:f(v)}")
        return map_dict
        
    def validate_homomorphism(self, map, image=None):
        """Checks that a dictionary defines a graph homomorphism"""
        if image==None:
            print "No image graph provided."
            for vertex in self.vertices():
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
         
    