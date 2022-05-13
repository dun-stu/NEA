import hashlib
import pygame, sys
import math
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
import json
pygame.init()


def check_cycle(StartNode, NodeFrom, List, D):
    for EachConnection in D[StartNode[0]]:
        if EachConnection != NodeFrom:
            if EachConnection in List:
                """used for testing
                print(EachConnection)
                #pygame.draw.circle(screen, (0, 0, 0), EachConnection, 4) #to be changed
                #screen.blit(map, (0,0,0))
                #pygame.display.update()
                #breakpoint()
                """
                return True
            List.append(EachConnection)
            C  = check_cycle(EachConnection, [StartNode[0], EachConnection[1]] , List, D)
           # print(E)
            if C == True: return C

    return False

def cant_select(msg, showing=False):
    popup = tk.Tk()
    popup.wm_title("") 
    ttk.Label(popup, text=msg, font=("Verdana", 20)).pack(side="top", fill="x", pady=10)       
    Button(popup, text="OK",  width=12 , command = popup.destroy).pack(pady="5") 
    
def check_vertex(CoordinateSet1, CoordinateSet2, Version = 1): #to check if the lines between two sets of coordinates intersect
  
    x1_1 = CoordinateSet1[0][0] #x value of the first coordinate
    x1_2 = CoordinateSet1[1][0] #x value of the second coordinate
     
    y1_1 = CoordinateSet1[0][1] #y value of the first coordinate
    y1_2 = CoordinateSet1[1][1] #y value of the second coordinate

    try:
        m1 = (y1_2 - y1_1)/(x1_2 - x1_1) #gradient
    except ZeroDivisionError:
        m1 = math.inf                   #if vertical line

    if isinstance(CoordinateSet2[0], list): # checking two sets of co-ordnates
        x2_1 = CoordinateSet2[0][0]
        x2_2 = CoordinateSet2[1][0]

        y2_1 = CoordinateSet2[0][1]
        y2_2 = CoordinateSet2[1][1]
        
        try:
            m2 = (y2_2 - y2_1)/(x2_2 - x2_1)
        except ZeroDivisionError:
            m2 = math.inf
    
        if m1 == m2: # if gradients the same
            """used for testing
            print('gradients the same') 
            """
            return False #no (proper) intersection

        #maths demonstrated in design
        if math.isinf(m1):
            x = x1_1
            y = (m2*(x - x2_1)) + y2_1
        elif math.isinf(m2):
            x = x2_1
            y = (m1*(x - x1_1)) + y1_1
        else:
            x = (y2_1-y1_1+(m1*x1_1)-(m2*x2_1))/(m1 - m2) 
            y = (m1*(x - x1_1)) + y1_1

        if  (min(x1_1,x1_2) <= x <= max(x1_1,x1_2)) and (min(x2_1,x2_2) <= x <= max(x2_1,x2_2)) and (min(y1_1,y1_2) <= y <= max(y1_1,y1_2)) and (min(y2_1,y2_2) <= y <= max(y2_1,y2_2)):
            return (x,y) #if the coordinates are within the correct range of each other 
        else:
            """used for testing
            print('intersections outside coordinate ranges')
            """
            return False
    elif isinstance(CoordinateSet2[0], float) or isinstance(CoordinateSet2[0], int): #to check if a third coordinate is between two, if co-ordinate set 2, is just a co-ordinate ⓵ ⓶
        if (min(x1_1,x1_2) <= CoordinateSet2[0] <= max(x1_1,x1_2)) and ((min(y1_1,y1_2) <= CoordinateSet2[1] <= max(y1_1,y1_2))): #⓷
            #if the third coordinate is between the other two coordinates
            try:
                m2 = (CoordinateSet2[1] - y1_1)/(CoordinateSet2[0] - x1_1)
            except ZeroDivisionError:
                m2 = math.inf
                #if the gradients are the same, or the third coordinate IS one of the others
            if (round(m1, 4) == round(m2, 4)) or (CoordinateSet2 == tuple(CoordinateSet1[0])) or (CoordinateSet2 == tuple(CoordinateSet1[1])):  #⓸
                return True #⓹	

                """used for testing
            elif (m1 != m2):
                print('m1 = ', end = "")
                print(m1)
                print('m2 = ', end = "")
                print(m2)
                """ 
            """used for testing
        else:
            print('(third) coordinate outside coordinate ranges')
            """
        return False #⓺

def distance_between(Point1, Point2):
    return math.sqrt(((Point1[0] - Point2[0])**2) + ((Point1[1] - Point2[1])**2))

class edge():

    def __init__(self, Key, value):
        self.node1    = Key
        self.node2    = value[0]
        self.distance = value[1]
 
class map_class:
    
    def __init__(self, Lines): #constructor, takes in the lines
        self.Lines  = Lines
        self.Nodes  = []
        self.graph  = {} 
        self.colour = (192,192,192)
        self.algorithm = None

    def get_nodes(self, endnodes):
            """used for testing
            print(len(self.Lines))
            """
            
            for l in range(0, (len(self.Lines))): #go through every line on the screen
                if endnodes:    #add the endpoints of lines too
                    self.Nodes.append(tuple(self.Lines[l][0]))
                    self.Nodes.append(tuple(self.Lines[l][len(self.Lines[l])- 1]))

                for c in range(0, (len(self.Lines[l])-1)): #go through every coordinate in the current line, it and it's immediate consecutive to be used, 
                    #so c won't = the final coordinate in a line
                    for l2 in range(l, (len(self.Lines))): #⓵
                        if l2 == l: #if the line in the same line of the original coordinate
                            c1 = c  #⓶
                        else:
                            c1 = 0
                        for c2 in range(c1, (len(self.Lines[l2])-1)):
                            Node = check_vertex([self.Lines[l][c],self.Lines[l][c+1]],[self.Lines[l2][c2],self.Lines[l2][c2+1]])
                            #returns false if no intersection, or returns the point of intersection
                            #see if the coordinate pairning of the the coordinate index c in line l (and the next coordinate along in that line)
                            #intersects with the coordinate pairning of the the coordinate index c2 in line l2 (and the next coordinate along in that line))
                            if Node == False: 
                                pass
                            elif (self.Lines[l][c+1] == self.Lines[l2][c2]) and (l2 == l): #if comparing two adjacent nodes, with the next two adjacent to those in the same line
                                pass
                            
                            else: #if valid node from intersection
                                for EachVertex in self.Nodes: 
                                    if Node == EachVertex: #if node already present, say if the method already called for example
                                        Node = False

                                """used for testing
                                print([self.Lines[l][c],self.Lines[l][c+1]],[self.Lines[l2][c2],self.Lines[l2][c2+1]])
                                """
                                if Node == False:
                                    pass
                                else:
                                    Node = tuple(Node)
                                    self.Nodes.append(Node) #Node recorded

    def get_connections(self):  

        for EachNode in self.graph.keys(): # the connections for each node is gotten
            """used for testing
            print('EachNode = ', end = "")
            print(EachNode)
            """
            for EachLine in self.Lines: #the node may be in, and have multiple connections in whichever lines it is in
                for v1 in range(0,(len(EachLine) - 1)):
                    """used for testing
                    #print('EachNode = ', end = "")
                    #print(EachNode)
                    print('tuple(EachLine[v1]) = ', end = "")
                    print(tuple(EachLine[v1]))

                    """
                    if check_vertex((EachLine[v1],EachLine[v1 + 1]),EachNode): #get the location if the nodes
                        """used for testing
                        print(EachNode, end = "")
                        print(" found")
                        print('tuple(EachLine[v1]) = ', end = "")
                        print(tuple(EachLine[v1]))
                        print('tuple(EachLine[v1 + 1]) = ', end = "")
                        print(tuple(EachLine[v1 + 1]))
                        """ 
                       
                        nc = False
                        
                        for EachVertex in self.graph.keys(): 
                            """used for testing
                            print(EachVertex)
                            """ 
                            if check_vertex((EachLine[v1],EachNode), EachVertex): #check if there is another node between the node and the nearest prior coordinate
                                d = distance_between(EachVertex, EachNode)
                                if round(d,1) != 0:   #if that node isn't itself
                                    nc = True          # so you don't need to find the nearest connection prior, it is found
                                    self.graph[EachNode].append([EachVertex, round(d,6)])
                        
                        d = distance_between(EachLine[v1], EachNode)
                        
                        for v2 in range((v1), 0,-1): #checks for connections chronologically prior in the list
                            
                            if nc == True: break #if connection prior found

                            for EachVertex in self.graph.keys(): #check if any other nodes are present
                                if check_vertex((EachLine[v2],EachLine[v2 - 1]),EachVertex): #checks if there is another node
                                    d += distance_between(EachLine[v2],EachVertex) #add the distance between the found node and the last recorded coordinate
                                    if round(d,1) != 0: #if the 
                                        self.graph[EachNode].append([EachVertex,round(d,6)])
                                        nc = True
                                        break  

                            else: d += distance_between(EachLine[v2],EachLine[v2 - 1]) #if not then the distance between the two adjacent coordinates checked is added
                                      
                        nc = False #reset
                        #same logic as before, but checking for the next node after the current one in the list
                        for EachVertex in self.graph.keys():  #check if there is another node between the node and the nearest next coordinate 
                            if check_vertex((EachLine[v1+1],EachNode), EachVertex):
                                d = distance_between(EachVertex, EachNode)
                                if round(d,1) != 0:
                                    nc = True
                                    self.graph[EachNode].append([EachVertex, round(d,6)])
                       
                        d = distance_between(EachLine[v1+1], EachNode)
                        for v2 in range((v1+1), (len(EachLine)-1)):#checks for connections chronologically after in the list
                            if nc == True: break

                            for EachVertex in self.graph.keys():
                                if check_vertex((EachLine[v2],EachLine[v2 + 1]),EachVertex):
                                    """used for testing
                                    print('tuple(EachLine[v2]) = ', end = "")
                                    print(tuple(EachLine[v2]))
                                    print('tuple(EachLine[v2 + 1]) = ', end = "")
                                    print(tuple(EachLine[v2 + 1]))
                                    print('EachVertex = ' ,end = "")
                                    print(EachVertex)
                                    """ 
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0:
                                        self.graph[EachNode].append([EachVertex,round(d,6)])
                                        nc = True
                                        break

                            else: 
                                d += distance_between(EachLine[v2],EachLine[v2 + 1]) #adds the distance of the adjacent coordinates checked, if no node found
                                """used for testing
                                print(d)
                                """

                        """used for testing
                    else: breakpoint()
                    """

        for each in self.graph.keys():  #remove duplicates
            temp = []

            for i in self.graph[each]:
                if i not in temp:
                    temp.append(i)

            self.graph[each] = temp
            
    def make_graph(self, endnodes = True): #default with endnodes present 
        self.get_nodes(endnodes) #get the nodes ⓵
        self.graph = {EachNode:[] for EachNode in self.Nodes} #create the initial qualities of the graph ⓶
        self.get_connections() #add the connections to the graph⓷

        InitKeys = {key: self.graph[key] for key in self.graph.keys()}

        for EachKey in InitKeys: #rounding all the nodes ⓸
            self.graph[(round(EachKey[0], 6), round(EachKey[1], 6))] = self.graph.pop(EachKey)
        
        del InitKeys

        for EachValue in self.graph: #rounding all the connections
            """used for testing
            print(self.graph[EachValue])
            """
            for ec in range(0, len(self.graph[EachValue])):
                self.graph[EachValue][ec][0] = (round(self.graph[EachValue][ec][0][0], 6), round(self.graph[EachValue][ec][0][1], 6) )

    def select_node(self, subgraph):
        global SubGraphLines
        SubGraphLines = self.get_algorithm_lines(subgraph, subgraph) #⓵
        Node = display_mapping_editor(self.Lines, self.colour, False, False, False, False, False, True) #⓷
        del SubGraphLines #try not to have excess global variables
        return Node

    def select_graph(self):
        global SubGraphs #global, so that it can be accessed by the mapping editor ⓵ 
        SubGraphs = [] #has all the subgraphs in a list ⓵
        ToBeFound = [] #⓶
        for EachNode in self.graph.keys(): #add all the nodes in a list⓶
            ToBeFound.append(EachNode) #to be found⓶

        while len(ToBeFound) != 0: #graph still needs traversing if there are still nodes to be found ⓻
            subgraph = {} #⓷
            queue = [ToBeFound[0]] #starting vertex for traversal
            while len(queue) != 0: #⓸
                for EachConnection in self.graph[queue[0]]: #goes through each of the connections to a node
                    if (EachConnection[0] in ToBeFound) and (EachConnection[0] not in queue):
                        queue.append(EachConnection[0]) #adds connections to the node, so they themselves can be checked for their connections

                ToBeFound.remove(queue[0]) #the node has been found and checked for connections
                subgraph.update({queue[0]:self.graph[queue[0]]}) #⓹
                #the node is part of the same subgraph as the rest in the iteration, as they are only added to the queue in the first place as they connect another node
                queue.pop(0) #so the next node in the list can be checked
            
            SubGraphs.append(subgraph) #⓺

        self.subgraph = display_mapping_editor(self.Lines,self.colour, False, False, True)

    def Prims(self, subgraph):
        Edges = []
        for EachKey in subgraph.keys():
            for EachValue in subgraph[EachKey]:
                Edges.append(edge(EachKey, EachValue))

        for EachEdge1 in Edges: #loop through all the edges
            n2 = 0
            for EachEdge2 in Edges:
                if ((EachEdge1.node1 == EachEdge2.node2) and
                    (EachEdge1.node2 == EachEdge2.node1) and
                    (EachEdge1.distance == EachEdge2.distance)): #if it is a duplicate, just with the nodes switched
                    Edges.remove(EachEdge2) #delete one of the duplicates
                    break
        MST = {}
        Edges.sort(key=lambda x: x.distance, reverse=False) #sorts Edges by distances
        edges = 0
        MST.update({Edges[random.randint(0,(len(Edges) - 1))].node1: ''}) #choose a random start node ⓵ ⓶
        while (edges < (len(subgraph.keys()) - 1)): #while num of edges < num of nodes - 1 ⓸
            for EachEdge in Edges:
                if (EachEdge.node1 in MST.keys()) ^ (EachEdge.node2 in MST.keys()): #XOR, so the smallest Edge, which conects and unvisited node(not in MST) to the MST is added
                    #adding the edges to the minimum spanning tree (as a dictionary) ⓶
                    try:    MST[EachEdge.node1].append([EachEdge.node2, EachEdge.distance])     #if the node has been added already  
                    except: MST.update({EachEdge.node1: [[EachEdge.node2, EachEdge.distance]]}) #if the node is not part of the spanning tree yet

                    try:    MST[EachEdge.node2].append([EachEdge.node1, EachEdge.distance]) 
                    except: MST.update({EachEdge.node2: [[EachEdge.node1, EachEdge.distance]]})  
                    if check_cycle([EachEdge.node2, EachEdge.distance], None, [[EachEdge.node2, EachEdge.distance]], MST): #⓷
                        MST[Edges[edgenumber].node1].pop()  #undoes adding the edge, if it does result in a cycle
                        MST[Edges[edgenumber].node2].pop()
                        if len(MST[Edges[edgenumber].node1]) == 0: del MST[Edges[edgenumber].node1] #if the node has no connections
                        if len(MST[Edges[edgenumber].node2]) == 0: del MST[Edges[edgenumber].node2] #it is redundant as a key
                    else: 
                        edges += 1 #records the extra edge added
              
                    """used for testing"""
                    global SubGraphLines
                    SubGraphLines = self.get_algorithm_lines(subgraph, MST)
                    display_mapping_editor(self.Lines, self.colour, False, False, False, False, True) #so the additions are made incrementally on the screen
                    """ """
                    break
        self.algorithmgraph = MST

    def Djikstra(self, subgraph):

        if len(subgraph.keys()) == 1: #if the subgraph is just a single point looped ⓵
             return subgraph           #then the shortest path from a point to itself is just the only path in the graph

        Node1 = None
        Node2 = None

        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        print('Node2:   ', end = "")
        print(Node2)
        """ 

        while Node1 == Node2: #no shortest path between a node and itself, except in case above ⓶
            #prompt to select node 
            popup = tk.Tk()
            popup.wm_title("") #https://pythonprogramming.net/
            ttk.Label(popup, text='Select the first Node', font=("Verdana", 50)).pack(side="top", fill="x", pady=10)
            ttk.Label(popup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)
            ttk.Button(popup, text="Okay", command = popup.destroy).pack()
            popup.mainloop()

            Node1 = tuple(self.select_node(subgraph)) #use select node method

            #popup to prompt you
            popup = tk.Tk()
            popup.wm_title("") 
            ttk.Label(popup, text='Select the second Node', font=("Verdana", 50)).pack(side="top", fill="x", pady=10)
            ttk.Label(popup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)
            ttk.Button(popup, text="Ok", command = popup.destroy).pack()
            popup.mainloop()

            Node2 = tuple(self.select_node(subgraph))


        t = time.time()

        #code to add the selected points as nodes to the subgraph   ⓶
        SubGraphLines = self.get_algorithm_lines(subgraph, subgraph) #get the graph as lines 
        subgraph = map_class(SubGraphLines)     #so the mapclass can be used
        subgraph.Nodes.append(tuple(Node1))     #to create a new subgraph but with the two points added
        subgraph.Nodes.append(tuple(Node2))     #as nodes
        subgraph.make_graph()
        subgraph = subgraph.graph
           
        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        print('Node2:   ', end = "")
        print(Node2)
        """ 
        #Optimising subgraph for this algorithm ⓷

        for EachKey in subgraph.keys():
            v1 = 0
            for EachValue1 in subgraph[EachKey]: #so if subgraph[EachKey] is shortened, it will end at the last value

                if subgraph[EachKey][v1][0] == EachKey: subgraph[EachKey].remove(subgraph[EachKey][v1]) #if there is a loop from a point to itself, and that isn't the whole subgraph
                v2 = 0
                for EachValue2 in subgraph[EachKey]:
                    if subgraph[EachKey][v1][0] == subgraph[EachKey][v2][0]: #if a node connects to another one twice
                        if   subgraph[EachKey][v1][1] > subgraph[EachKey][v2][1]: 
                            subgraph[EachKey].remove(subgraph[EachKey][v1])
                            v1 -= 1

                        elif subgraph[EachKey][v1][1] < subgraph[EachKey][v2][1]:
                           subgraph[EachKey].remove(subgraph[EachKey][v2])
                           v1 -= 1

                    v2 += 1
                        #the larger connection is removed, as this will never be utilised in a shortest path
                v1 += 1

        #defaults
        Unvisited = [] 
        Visited   = []
        Table     = []
        for EachNode in subgraph.keys():
            Table.append([EachNode, math.inf, None]) # Node, distance, previous node 
            """used for testing
            print([EachNode, math.inf, None])
            """ 
            Unvisited.append(EachNode)      #initially all nodes are unvisited
        
        NextNode = Node1
        d = 0
        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        print('Node2:   ', end = "")
        print(Node2)
        """ 

        Table[[Table[i][0] for i in range(0,len(Table))].index(NextNode)][1] = 0 #distance from a node to itself is 0

        while len(Visited) != len(subgraph.keys()): #there is still unvisited nodes
            """used for testing
            print('Table:')
            for Each in Table:  
                print(Each)
            print()
            """
            for EachValue in subgraph[NextNode]: #all that connect to the node being visited

                valueindex = [Table[i][0] for i in range(0,len(Table))].index(EachValue[0])  #where a node is in a table
                
                if (d + EachValue[1]) < Table[valueindex][1]:   #if this new distance is more than the previous distance
                    Table[valueindex][1] = d + EachValue[1]     
                    Table[valueindex][2] = NextNode             #previous node 

            """used for testing
            print('Next Node:   ',end = "")
            print(NextNode)
            #print('Unvisited:   ',end = "")
            #print(Unvisited)
            """ 

            Visited.append(NextNode)
            #Unvisited.remove(NextNode)

            d = math.inf 
            for key in range(0,len(Table)): #get the unvisited node with the lowest distance to visit
                if (Table[key][1] < d) and (Table[key][0] not in Visited):  #if the key is unvisited and it's distance is the lowest one yet
                    d = Table[key][1]        
                    NextNode = Table[key][0] #next node to visit

        #converting the path between Node1 and Node 2 into a dictionary
        NextNode = Node2
        algorithmgraph = {}
        while NextNode != Node1: #Each line in the path from Node2 to Node1 will be added

            valueindex = [Table[i][0] for i in range(0,len(Table))].index(NextNode)

            for EachConnection in subgraph[NextNode]: #get the connection 
                if Table[valueindex][2] == EachConnection[0]: #to the previous node in the path
                    break #EachConnection will be the previous Node connection when break

            try:    algorithmgraph[NextNode].append(EachConnection)     #if the node has been added already  
            except: algorithmgraph.update({NextNode: [EachConnection]}) #if the node is not part of the dictionary yet

            try:    algorithmgraph[EachConnection[0]].append([NextNode, EachConnection[1]]) 
            except: algorithmgraph.update({EachConnection[0]: [[NextNode, EachConnection[1]]]})

            NextNode = EachConnection[0]

        #print(algorithmgraph)
        #print(subgraph)
        self.algorithmgraph = algorithmgraph
        """used for testing"""
        print('time elapsed = ' + str(time.time() - t))
        """ """
        #https://pythonprogramming.net/
    def breadth_first(self, subgraph):

        if len(subgraph.keys()) == 1: #if the subgraph is just a single point looped    ⓵
             return subgraph           #then the shortest path from a point to itself is just the only path in the graph
        Node1 = None
        #prompt to select node  
        popup = tk.Tk()
        popup.wm_title("") 
        ttk.Label(popup, text='Select the start Node', font=("Verdana", 50)).pack(side="top", fill="x", pady=10)
        ttk.Label(popup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)
        ttk.Button(popup, text="Okay", command = popup.destroy).pack()
        popup.mainloop()
        Node1 = tuple(self.select_node(subgraph))   #⓶
        t = time.time()
        #code to add the selected points as nodes to the subgraph
        SubGraphLines1 = self.get_algorithm_lines(subgraph, subgraph) #get the graph as lines 
        subgraph = map_class(SubGraphLines1)     #so the mapclass can be used
        subgraph.Nodes.append(tuple(Node1))     #to create a new subgraph but with the two points added
        subgraph.make_graph()
        subgraph = subgraph.graph
        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        """
        #Optimising subgraph for this algorithm ⓷
        for EachKey in subgraph.keys():
            v1 = 0
            for EachValue1 in subgraph[EachKey]: #so if subgraph[EachKey] is shortened, it will end at the last value

                if subgraph[EachKey][v1][0] == EachKey: subgraph[EachKey].remove(subgraph[EachKey][v1]) #if there is a loop from a point to itself, and that isn't the whole subgraph
                v2 = 0
                for EachValue2 in subgraph[EachKey]:
                    if subgraph[EachKey][v1][0] == subgraph[EachKey][v2][0]: #if a node connects to another one twice
                        if   subgraph[EachKey][v1][1] > subgraph[EachKey][v2][1]: subgraph[EachKey].remove(subgraph[EachKey][v1])

                        elif subgraph[EachKey][v1][1] < subgraph[EachKey][v2][1]: subgraph[EachKey].remove(subgraph[EachKey][v2])
                    v2 += 1
                        #the larger connection is removed, as this will never be utilised in a shortest path
                v1 += 1

        algorithmgraph = {}
        queue = [Node1] 
        #Unvisited = [EachNode for EachNode in subgraph.keys()]
        
        while len(queue) != 0: #not empty #⓹
            VisitingNode = queue[0] #move onto the next Node on top of the stack ⓸

            for EachConnection in subgraph[VisitingNode]: #⓷
                if EachConnection[0] not in algorithmgraph.keys():
                    try:    algorithmgraph[VisitingNode].append(EachConnection)     #if the node has been added already  
                    except: algorithmgraph.update({VisitingNode: [EachConnection]}) #if the node is not part of the dictionary yet
                    #⓶ 
                    try:    algorithmgraph[EachConnection[0]].append([VisitingNode, EachConnection[1]])   #connection needs to be added on both 
                    except: algorithmgraph.update({EachConnection[0]: [[VisitingNode, EachConnection[1]]]}) #nodes' key value pair
                    """used for testing
                    print('VisitingNode:    ',end="")
                    print(VisitingNode)
                    print('EachConnection[0]:   ',end="")
                    print(EachConnection[0])
                    #print('Unvisited:   ',end="")
                    #print(Unvisited)
                    print('Stack:   ',end="")
                    print(Stack)
                    """ 
                    #Unvisited.remove(VisitingNode)
                    queue.append(EachConnection[0])     #⓵
                    """used for testing
                    print('Stack:   ',end="")
                    print(Stack)
                    """ 

                    global SubGraphLines
                    SubGraphLines = self.get_algorithm_lines(subgraph, algorithmgraph) 
                    display_mapping_editor(self.Lines, self.colour, False, False, False, False, True)
                    #displays the updated situation of the spanning tree
                  
            else: queue.pop(0) # if none of the connections are Unvisited

        self.algorithmgraph = algorithmgraph
        """used for testing
        print('time elapsed = ' + str(time.time() - t))
        """ 

    def kruscals(self, subgraph):

        t = time.time()
        Edges = []
        for EachKey in subgraph.keys():
            for EachValue in subgraph[EachKey]:
                Edges.append(edge(EachKey, EachValue))

        for EachEdge1 in Edges: #loop through all the edges
            n2 = 0
            for EachEdge2 in Edges:
                if ((EachEdge1.node1 == EachEdge2.node2) and
                    (EachEdge1.node2 == EachEdge2.node1) and
                    (EachEdge1.distance == EachEdge2.distance)): #if it is a duplicate, just with the nodes switched
                    Edges.remove(EachEdge2) #delete one of the duplicates
                    break

        Edges.sort(key=lambda x: x.distance, reverse=False) #sorts Edges by distances
        """used for testing
        print(subgraph)
        for e in range(0,len(Edges)):
            print(( str(Edges[e].node1) + ' , ' + str(Edges[e].distance) + ' , ' + str(Edges[e].node2) ) )
        
        """ 

        MST = {} #Minimum spanning tree
        edgenumber   = 0 #index of the next smallest edge
        edges = 0 #number of edges
        while (edges < (len(subgraph.keys()) - 1)): #while num of edges < num of nodes - 1 ⓷

            #adding the edges to the minimum spanning tree (as a dictionary)
            try:    MST[Edges[edgenumber].node1].append([Edges[edgenumber].node2, Edges[edgenumber].distance])     #if the node has been added already  
            except: MST.update({Edges[edgenumber].node1: [[Edges[edgenumber].node2, Edges[edgenumber].distance]]}) #if the node is not part of the spanning tree yet
            
            try:    MST[Edges[edgenumber].node2].append([Edges[edgenumber].node1, Edges[edgenumber].distance]) 
            except: MST.update({Edges[edgenumber].node2: [[Edges[edgenumber].node1, Edges[edgenumber].distance]]})

            """used for testing
            print(MST)
            """ 
            if check_cycle([Edges[edgenumber].node2, Edges[edgenumber].distance], None, [[Edges[edgenumber].node2, Edges[edgenumber].distance]], MST): #⓵
                MST[Edges[edgenumber].node1].pop()  #undoes adding the edge, if it does result in a cycle
                MST[Edges[edgenumber].node2].pop()
                if len(MST[Edges[edgenumber].node1]) == 0: del MST[Edges[edgenumber].node1] #if the node has no connections
                if len(MST[Edges[edgenumber].node2]) == 0: del MST[Edges[edgenumber].node2] #it is redundant as a key
            else: 
                edges += 1 #records the extra edge added
              
                global SubGraphLines
                SubGraphLines = self.get_algorithm_lines(subgraph, MST)             
                display_mapping_editor(self.Lines, self.colour, False, False, False, False, True)
                #displays the updated situation of the spanning tree
                """ """
            edgenumber += 1 #⓶ as the list is in ascending order
        self.algorithmgraph = MST
        """used for testing"""
        print('time elapsed = ' + str(time.time() - t))
        """ """

    def depth_first(self, subgraph):

        if len(subgraph.keys()) == 1: #if the subgraph is just a single point looped
             return subgraph           #then the shortest path from a point to itself is just the only path in the graph

        Node1 = None


        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        """

        
        #prompt to select node 
        popup = tk.Tk()
        popup.wm_title("") #https://pythonprogramming.net/
        ttk.Label(popup, text='Select the start Node', font=("Verdana", 50)).pack(side="top", fill="x", pady=10)
        ttk.Label(popup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)
        ttk.Button(popup, text="Okay", command = popup.destroy).pack()
        popup.mainloop()

        Node1 = tuple(self.select_node(subgraph))

        #code to add the selected points as nodes to the subgraph
        SubGraphLines1 = self.get_algorithm_lines(subgraph, subgraph) #get the graph as lines 
        subgraph = map_class(SubGraphLines1)     #so the mapclass can be used
        subgraph.Nodes.append(tuple(Node1))     #to create a new subgraph but with the two points added
        subgraph.make_graph()
        subgraph = subgraph.graph
        
        
        """used for testing
        print('Node1:   ', end = "")
        print(Node1)
        """

        #Optimising subgraph for this algorithm

        for EachKey in subgraph.keys():
            v1 = 0
            for EachValue1 in subgraph[EachKey]: #so if subgraph[EachKey] is shortened, it will end at the last value

                if subgraph[EachKey][v1][0] == EachKey: subgraph[EachKey].remove(subgraph[EachKey][v1]) #if there is a loop from a point to itself, and that isn't the whole subgraph
                v2 = 0
                for EachValue2 in subgraph[EachKey]:
                    if subgraph[EachKey][v1][0] == subgraph[EachKey][v2][0]: #if a node connects to another one twice
                        if   subgraph[EachKey][v1][1] > subgraph[EachKey][v2][1]: subgraph[EachKey].remove(subgraph[EachKey][v1])

                        elif subgraph[EachKey][v1][1] < subgraph[EachKey][v2][1]: subgraph[EachKey].remove(subgraph[EachKey][v2])
                    v2 += 1
                        #the larger connection is removed, as this will never be utilised in a shortest path
                v1 += 1

        algorithmgraph = {}
        Stack = [Node1] #⓵
        #Unvisited = [EachNode for EachNode in subgraph.keys()]
        
        while len(Stack) != 0: #not empty 	⓺
            VisitingNode = Stack[len(Stack) -1] #move onto the next Node on top of the stack

            for EachConnection in subgraph[VisitingNode]: #⓷	
                if EachConnection[0] not in algorithmgraph.keys(): #⓷, if it is visited, it would have been added to the algorithm graph
                    try:    algorithmgraph[VisitingNode].append(EachConnection)     #if the node has been added already  
                    except: algorithmgraph.update({VisitingNode: [EachConnection]}) #if the node is not part of the dictionary yet

                    try:    algorithmgraph[EachConnection[0]].append([VisitingNode, EachConnection[1]]) 
                    except: algorithmgraph.update({EachConnection[0]: [[VisitingNode, EachConnection[1]]]})
                    """used for testing
                    print('VisitingNode:    ',end="")
                    print(VisitingNode)
                    print('EachConnection[0]:   ',end="")
                    print(EachConnection[0])
                    #print('Unvisited:   ',end="")
                    #print(Unvisited)
                    print('Stack:   ',end="")
                    print(Stack)
                    """ 
                    #Unvisited.remove(VisitingNode)
                    Stack.append(EachConnection[0])
                    """used for testing
                    print('Stack:   ',end="")
                    print(Stack)
                    """ 
                    global SubGraphLines
                    SubGraphLines = self.get_algorithm_lines(subgraph, algorithmgraph)
                    display_mapping_editor(self.Lines, self.colour, False, False, False, False, True)
                    break #⓸, as this will force the same thing to happen to the node just appended to the stack
                    
            else: Stack.pop() # if none of the connections are Unvisited ⓹

        self.algorithmgraph =  algorithmgraph
                #https://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed
    def perform_algorithm(self):

        #prompt to select subgraph 
        popup = tk.Tk()
        popup.wm_title("") 
        ttk.Button(popup, text="    Select subgraph     ", command = lambda:[popup.destroy(), self.select_graph()]).pack() #allow subgraph to be selected 	⓵      
        ttk.Label(popup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)       
        popup.mainloop()        
         
        cycle = check_cycle(list(self.subgraph.values())[0][0], None, [list(self.subgraph.values())[0][0]], self.subgraph) # ⓶ 
        
        popup = tk.Tk()
        popup.wm_title("")  
        ttk.Label(popup, text=' Select an algorithm to perform ', font=("Verdana", 40)).pack(side="top", fill="x", pady=10)
        
        if cycle: #if not a tree, colour is white, when selected the algorithm is called, ⓷ ⓸
            Button(popup, text="      Prims         ",  width=12 , bg=OnButtonColour, command = lambda:[popup.destroy(),      self.Prims(self.subgraph)    ]).pack(pady="5")
            Button(popup, text="     kruscals       ",  width=12 , bg=OnButtonColour, command = lambda:[popup.destroy(),    self.kruscals(self.subgraph)   ]).pack(pady="5") 
        else:    #if not a tree, colour is grey, when selected an error message appears
            errormessage = 'Cannot perform this algorithm on a Tree'
            Button(popup, text="      Prims         ",  width=12 , bg=OffButtonColour, command = lambda:[cant_select(errormessage)]).pack(pady="5")
            Button(popup, text="     kruscals       ",  width=12 , bg=OffButtonColour, command = lambda:[cant_select(errormessage)]).pack(pady="5") 
       #all buttons, white, when pressed algorithm is called  ⓷ ⓸
        Button(popup, text="     Djikstra       ",  width=12 , bg=OnButtonColour, command = lambda:[popup.destroy(),    self.Djikstra(self.subgraph)   ]).pack(pady="5")
        Button(popup, text="    depth first     ",  width=12 , bg=OnButtonColour, command = lambda:[popup.destroy(),   self.depth_first(self.subgraph) ]).pack(pady="5")
        Button(popup, text="   breadth first    ",  width=12 , bg=OnButtonColour, command = lambda:[popup.destroy(), self.breadth_first(self.subgraph) ]).pack(pady="5")
        popup.mainloop()
        """used for testing
        print(subgraph)
         
        global SubGraphs
        del SubGraphs

        """
        """E used for testing
        print(C)
        return E
        """
        global SubGraphLines
        SubGraphLines = self.get_algorithm_lines(self.subgraph, self.algorithmgraph)
        """used for testing
        print(SubGraphLines)
        breakpoint()
        """ 
        display_mapping_editor(self.Lines, self.colour, False, False, False, False, True) #display the results, mode displaying algorithm
        del SubGraphLines #excess global variables
        del self.subgraph

    def get_algorithm_lines(self, subgraph, algorithmgraph):
        AlgorithmGraphLines = []
        for EachKey in algorithmgraph.keys(): 

            for EachLine in self.Lines: #possibly add Subgraphlines instead
                for v1 in range(0, (len(EachLine)-1)):
                   if check_vertex((EachLine[v1],  EachLine[v1 + 1]), EachKey):
                        """used for testing
                        print('EachKey:      ', end="")
                        print(EachKey)

                        """ 
                        nc = False
                        Line = []
                        Line.append(EachKey)
                        for EachVertex in subgraph.keys(): #
                                    if check_vertex((EachLine[v1 + 1],EachKey), EachVertex):
                                        d = distance_between(EachVertex, EachKey)
                                        if round(d,1) != 0:
                                            nc = True
                                            for EachValue in algorithmgraph[EachKey]:
                                                EachValue[1] = round(EachValue[1], 2)
                                                if [EachVertex, round(d,2)] == EachValue:  
                                                    Line.append(EachVertex)
                                                    AlgorithmGraphLines.append(Line)
                                                    break
                        #"""
                        d = distance_between(EachLine[v1 + 1], EachKey)
                        """used for testing
                        print('EachLine:  ', end ="")
                        print(EachLine)
                        """ 
                        for v2 in range((v1+1), (len(EachLine)-1)):
                            if nc == True: break
                            Line.append(EachLine[v2])

                            for EachVertex in subgraph.keys():
                                if nc == True: break
                                if check_vertex((EachLine[v2],EachLine[v2 + 1]),EachVertex):
                                    """used for testing
                                    print('tuple(EachLine[v2]) = ', end = "")
                                    print(tuple(EachLine[v2]))
                                    print('tuple(EachLine[v2 + 1]) = ', end = "")
                                    print(tuple(EachLine[v2 + 1]))
                                    print('EachVertex = ' ,end = "")
                                    print(EachVertex)
                                    """ 
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0:
                                        nc = True

                                        for EachValue in algorithmgraph[EachKey]:
                                            """used for testing
                                            print('[EachVertex, round(d,6)]:    ', end="")
                                            print([EachVertex, round(d,6)])
                                            """
                                             
                                            EachValue[1] = round(EachValue[1], 2)
                                            if [EachVertex, round(d,2)] == EachValue:  
                                                Line.append(EachVertex)
                                                AlgorithmGraphLines.append(Line)

                                                break
                            
                            else: 
                                d += distance_between(EachLine[v2],EachLine[v2 + 1])
                                """used for testing
                                print(d)
                                """
                        #breakpoint()
                        nc = False
                        Line = []
                        Line.append(EachKey)
                        for EachVertex in subgraph.keys(): #
                                    if check_vertex((EachLine[v1],EachKey), EachVertex):
                                        d = distance_between(EachVertex, EachKey)
                                        if round(d,1) != 0:
                                            nc = True
                                            for EachValue in algorithmgraph[EachKey]:
                                                EachValue[1] = round(EachValue[1], 2)
                                                if [EachVertex, round(d,2)] == EachValue:  
                                                    Line.append(EachVertex)
                                                    AlgorithmGraphLines.append(Line)
                        #"""
                        d = distance_between(EachLine[v1], EachKey)
                        for v2 in range((v1), 0, -1):

                            if nc == True: break
                            Line.append(EachLine[v2])
                            for EachVertex in subgraph.keys():
                                if nc == True: break
                                if check_vertex((EachLine[v2],EachLine[v2 - 1]),EachVertex):
                                    """used for testing
                                    print('tuple(EachLine[v2]) = ', end = "")
                                    print(tuple(EachLine[v2]))
                                    print('tuple(EachLine[v2 - 1]) = ', end = "")
                                    print(tuple(EachLine[v2 - 1]))
                                    print('EachVertex = ' ,end = "")
                                    print(EachVertex)
                                    """ 
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0:
                                        
                                        nc = True
                                        for EachValue in algorithmgraph[EachKey]:
                                            """used for testing
                                            print('[EachVertex, round(d,6)]:    ', end="")
                                            print([EachVertex, round(d,6)])
                                            print('EachValue:    ', end="")
                                            print(EachValue)
                                            """ 
                                            EachValue[1] = round(EachValue[1], 2)
                                            if [EachVertex, round(d,2)] == EachValue:  
                                                Line.append(EachVertex)
                                                AlgorithmGraphLines.append(Line)
                                                """used for testing
                                                print('[EachVertex, round(d,6)]:    ', end="")
                                                print([EachVertex, round(d,6)])
                                                """ 
                                                break

                            else: 
                                
                                d += distance_between(EachLine[v2],EachLine[v2 - 1])
                                """used for testing
                                print(d)
                                """  
                        #breakpoint()
        
        #code to remove duplicates:
        TempLines = AlgorithmGraphLines  
        AlgorithmGraphLines = []
        for EachLine in TempLines:
            for e in range(0, len(EachLine) ):
                EachLine[e] = list(EachLine[e])

            if (EachLine not in AlgorithmGraphLines) and (EachLine[::-1] not in AlgorithmGraphLines): AlgorithmGraphLines.append(EachLine)    #https://www.programiz.com/python-programming/methods/list/reverse
               #if the line, or its reverse (since a line composed of the same coordinates is just the same line), hasn't been added yet
        return AlgorithmGraphLines 
        
def pressing(buttonposition, button, mouseposition):
   if (buttonposition[0]) < mouseposition[0] < (buttonposition[0] + (button.get_rect()).width) and (buttonposition[1]) < mouseposition[1] < (buttonposition[1] + (button.get_rect()).height): return True
   else: return False   

def md5hashing(str2hash):

    for x in range(0,5):
        str2hash = hashlib.md5(str2hash.encode()).hexdigest()
    return str2hash

def Save(Lines):
    userdirectory = os.path.join(os.getcwd(), str(account))
    if os.path.exists(os.path.join(userdirectory, 'Lines.json')): #if there is a directory called lines
        f = open(os.path.join(userdirectory, 'Lines.json'), "r")
        if json.load(f) == Lines:   #check if those lines are already present ⓵ 
            cant_select('graph already saved')
            f.close()
            return

        for l in range(1,100): #assume not gonna have > 100 saved files, if you do, then time to overwrite
            if not os.path.exists(os.path.join(userdirectory, 'Lines[' + str(l) + '].json')): #get the next available index to save the file 
                filename = 'Lines[' + str(l) + '].json'
                break
            else:
                f = open(os.path.join(userdirectory, 'Lines[' + str(l) + '].json'), "r") #check if each file has the lines that are present currently ⓵
                if json.load(f) == Lines:  
                    cant_select('graph already saved') #error message
                    f.close()
                    return

    else: filename = 'Lines.json'

    Saved = tk.Tk()
    Saved.wm_title("") 
    ttk.Label(Saved, text=(str(filename) + ' has been saved'), font=("Verdana", 20)).pack(side="top", fill="x", pady=10)       
    Button(Saved, text="OK",  width=12 , command = Saved.destroy).pack(pady="5") 
    Saved.mainloop()

    f = open(os.path.join(userdirectory, filename), "w") #⓶ 
    f.write(str(Lines)) 
    f.close()

def display_mapping_editor(Lines = [], colour = (192,192,192), 
                           editing = True, makinggraph = False, 
                           selectinggraph = False, selectingalgorithm = False, 
                           displayingalorithm = False, selectingnodes = False, selectinglines = False):  

    #Editor is a function with different modes
    
    #pygame.time.Clock().tick(100)

    #Varying functionality allowed depending on the mode
    if makinggraph:
        lgbutton = False #logoff button
        svbutton = False #save button
        mgbutton = False #make graph button
        canpan   = True
        canzoom  = True
        candraw  = False
        pabutton = False #perform algorithm button

    if selectingalgorithm or selectinggraph or displayingalorithm or selectingnodes or selectinglines:
        lgbutton = False
        svbutton = False
        mgbutton = False #make graph button
        canpan   = False
        canzoom  = False
        candraw  = False
        pabutton = False #perform algorithm button
    
    if selectingnodes:
        linenumber       = 0 #for the index of the coordinate being highlighted
        coordinatenumber = 0
        next  = False #defaults
        prior = False

    if editing: #if in editing mode
        lgbutton = True #logoff button
        svbutton = True
        mgbutton = True #makinggraph 
        canpan   = True
        canzoom  = True
        candraw  = True
        pabutton = True

    screen  = pygame.display.set_mode((1536,800))
    #Permenant screen elements created

    optionsbar  = pygame.Surface((1536,100))    
    optionsbar.fill(colour)
    #Options bar with text
    optionstext = (pygame.font.SysFont('arial', 52)).render('OPTIONS', True, (0,0,0))

    MapSize = (1536, 700)
    map     = pygame.Surface(MapSize)
    map.fill((255,255,255))   # map only colour option is white, as this is clearest to draw on 
    #the surface to draw on

    mapbox  = pygame.transform.scale(map, [192, 88]) #the mapbox is the map surface scaled down by 8   ⓵
    MapBoxPosition        = (1100,6) #⓶
    #A small image showing the whole drawing surface for positional awareness during panning/zooming

    #defaults for the buttons
    GraphButtonTextColour = OffButtonTextColour
    GraphButtonColour     = OffButtonColour
    GraphButtonPosition   = (750,10)            #position on the screen

    UndoButtonTextColour  = OffButtonTextColour
    UndoButtonColour      = OffButtonColour
    UndoButtonPosition    = (1390,10)

    RedoButtonTextColour  = OffButtonTextColour
    RedoButtonColour      = OffButtonColour
    RedoButtonPosition    = (1460,10)

    PerformAlgorithmTextColour     = OffButtonTextColour #defaults
    PerformAlgorithmButtonColour   = OffButtonColour
    PerformAlgorithmButtonPosition = (710,55) #position on the screen

    SaveButtonPosition   = (500,30) #defaults
    SaveButtonTextColour = OffButtonTextColour
    SaveButtonColour     = OffButtonColour #position on the screen
        
    LogoffButtonPosition   = (300,30)   #defaults
    LogoffButtonTextColour = OffButtonTextColour
    LogoffButtonColour     = OffButtonColour

    zoomtext    = (pygame.font.SysFont('arial', 16)).render('      Zoom        ', True, (0,0,0)) 

    ZoomTextPosition = (1410,45)
    ZoomPercentagePosition    = (1440,70)
     
    ZoomUpTextColour        = OnButtonTextColour
    ZoomUpButtonColour      = OnButtonColour
    ZoomUpButtonPosition    = (1475,70)

    ZoomDownTextColour  = OffButtonTextColour
    ZoomDownButtonColour      = OffButtonColour
    ZoomDownButtonPosition    = (1400,70)
    
    """used for testing
    x = 500
    y = 0
    Points = [(x,y)]
    for x in range(500,1000):
        y = round(-((x-750)**2)/100 + 500)
        Points.append((x,y))

    print(Points)

    pygame.draw.lines(map, colour, False ,Points) #test
    """

    MapToScreenOffset = [0,100] #default #for testing

    displaying = True
    panning    = False
    zooming    = False
    drawing    = False
    ctrl       = False
    zoom       = 1
    zoomplus   = False
    linesexist = False

    t = time.time()
    S = 0 # which subgraph on
    """used for testing
    P = ['x value not relevant', 0] #test for panning
    K = [0,0] #test for panning 
    """
    E = None #E used for testing

    while displaying:

        """used for testing
        map = pygame.Surface(MapSize)
        map.fill((255,255,255))          # map only colour option is white, as this is clearest to draw on


        x = 500
        y = 0
        Points = [(x,y)]
        for x in range(500,1000):
        
            y = round(-((x-750)**2)/100 + 500)
            Points.append((x,y))


        pygame.draw.lines(map, colour, False ,Points, width = 10)
        """

        #code in progress
        map = pygame.Surface(MapSize)
        map.fill((255,255,255)) 
        try:     #try except used, in case there is no lines yet
            linesexist = False
            for EachLine in Lines:
                linesexist = True #if there is a line in Lines
                pygame.draw.lines(map, colour, False ,EachLine, width = 5)
            
            
            if len(NewLine) > 1: #a single coordinate is not valid as a line
                pygame.draw.lines(map, colour, False ,NewLine, width = 5) #if the NewLine hasn't been made yet, then this can't be run 
                linesexist = True #if there is a newline

        except:
            pass
        
        try:
            for EachNode in mapobject.Nodes:
                pygame.draw.circle(map, (0, 0, 0), EachNode, 4) #to be changed
            
            """used for testing
            screen.blit(map, MapToScreenOffset)
            pygame.display.update()

            input('test get connections')

            for EachKey in mapobject.graph.keys():
                
                pygame.draw.circle(map, (66, 66, 245), EachKey, 10)
                print(EachKey)
                
                
                for EachConnection in mapobject.graph[EachKey]:
                    pygame.draw.circle(map, (66, 245, 66), EachConnection[0], 5)
                
                screen.blit(map, MapToScreenOffset)
                pygame.display.update()
                input('next node')
                for EachNode in mapobject.Nodes: pygame.draw.circle(map, (0, 0, 0), EachNode, 10)

            """

        except: pass

        if displayingalorithm or selectingnodes:
            #⓵
            for EachLine in globals()['SubGraphLines']: #go through the edges in the subgraph
                pygame.draw.lines(map, (3, 123, 252) , False ,EachLine, width = 5) #draw each line in blue

        if displayingalorithm:
            for EachNode in [EachVertex[0] for EachVertex in globals()['SubGraphLines'] ]: #the nodes highlighted
                pygame.draw.circle(map, (66, 245, 66), EachNode, 4) #in green

            for EachNode in [EachVertex[len(EachVertex)-1] for EachVertex in globals()['SubGraphLines'] ]:
                pygame.draw.circle(map, (66, 245, 66), EachNode, 4) 

        if selectingnodes:
            linenumber = linenumber % len(globals()['SubGraphLines']) #if on last edge cycle to first
            Node = globals()['SubGraphLines'][linenumber][coordinatenumber] #⓸
            pygame.draw.circle(map, (66, 245, 66), Node, 4) #draw the Node  #⓹

        if selectinggraph:
            """
            try:
                SubGraphLines = []
                for EachNode in list(SubGraphs[S].keys()):

                    for EachLine in Lines:
                        if ((max(EachLine[l][0] for l in range(0,len(EachLine))) >= EachNode[0] >= min(EachLine[l][0] for l in range(0,len(EachLine)))) and
                            (max(EachLine[l][1] for l in range(0,len(EachLine))) >= EachNode[1] >= min(EachLine[l][1] for l in range(0,len(EachLine))))):
                                for c in range(0, EachLine - 1):
                                    if check_vertex((EachLine[c], EachLine[c+1]), EachNode):
                                        if EachLine not in SubGraphLines: SubGraphLines.append(EachLine)


                for EachLine in SubGraphLines:
                    pygame.draw.lines(map, (3, 123, 252) , False ,EachLine, width = 5)
                
            except:  pass    
            """
            """
            if round(((time.time() - t) % 2),1) == 0:
                time.sleep(0.2)
                S += 1
            
            """
            S = S % len(SubGraphs) #to decide which subgraph is being output
          
            SubGraphLines = [] 
            
            for EachNode in list(SubGraphs[S].keys()):

                 for EachLine in Lines:
                     if ((max(EachLine[l][0] for l in range(0,len(EachLine))) >= EachNode[0] >= min(EachLine[l][0] for l in range(0,len(EachLine)))) and #if the node is in
                        (max(EachLine[l][1] for l in range(0,len(EachLine))) >= EachNode[1] >= min(EachLine[l][1] for l in range(0,len(EachLine))))):  #the range of the line
                         for c in range(0, len(EachLine) - 1):
                             if check_vertex((EachLine[c], EachLine[c+1]), EachNode): #check if the node is on the line, 
                                 if EachLine not in SubGraphLines: SubGraphLines.append(EachLine) #dont put lines in twice


            for EachLine in SubGraphLines: #draw the lines of the the subgraph in blue
                 pygame.draw.lines(map, (3, 123, 252) , False ,EachLine, width = 5)

            for EachNode in SubGraphs[S].keys(): #draw the nodes of the subgraph in non black
                pygame.draw.circle(map, (65, 250, 65), EachNode, 4) 

        """ used for testing        
        try:
            SubGraphLines = []
            for EachNode in list(SubGraph.keys()):

                 for EachLine in Lines:
                     if ((max(EachLine[l][0] for l in range(0,len(EachLine))) >= EachNode[0] >= min(EachLine[l][0] for l in range(0,len(EachLine)))) and
                        (max(EachLine[l][1] for l in range(0,len(EachLine))) >= EachNode[1] >= min(EachLine[l][1] for l in range(0,len(EachLine))))):
                         for c in range(0, len(EachLine) - 1):
                             if check_vertex((EachLine[c], EachLine[c+1]), EachNode):
                                 if EachLine not in SubGraphLines: SubGraphLines.append(EachLine)

    
            for EachLine in SubGraphLines:
                 pygame.draw.lines(map, (245, 185, 66) , False ,EachLine, width = 5)

            for EachNode in SubGraph.keys():
                pygame.draw.circle(map, (65, 250, 65), EachNode, 4) #to be changed
        except:pass
        used for testing"""
        
        """ used for testing
        if isinstance(E, tuple): pygame.draw.circle(map, (245, 185, 66), E, 4) #to be changed
        """ 
        if linesexist and mgbutton: #⓶
            GraphButtonTextColour =  OnButtonTextColour
            GraphButtonColour     =  OnButtonColour
        else:
            GraphButtonTextColour =  OffButtonTextColour #if there are no lines, a graph can't be made
            GraphButtonColour     =  OffButtonColour

        if lgbutton:   #⓶
            LogoffButtonTextColour =  OnButtonTextColour
            LogoffButtonColour     =  OnButtonColour
        else:
            LogoffButtonTextColour =  OffButtonTextColour #if there are no lines, a graph can't be made
            LogoffButtonColour     =  OffButtonColour

        if linesexist and svbutton:   #⓶
            SaveButtonTextColour =  OnButtonTextColour
            SaveButtonColour     =  OnButtonColour
        else:
            SaveButtonTextColour =  OffButtonTextColour #if there are no lines, a graph can't be made
            SaveButtonColour     =  OffButtonColour
        
        try:
            mapobject = mapobject #if the graph has been made yet ⓶
            if pabutton: #if the current page allows this button
                PerformAlgorithmTextColour     = OnButtonTextColour
                PerformAlgorithmButtonColour   = OnButtonColour
        except:
                PerformAlgorithmTextColour     = OffButtonTextColour
                PerformAlgorithmButtonColour   = OffButtonColour

        if zoom < 3 and canzoom:
            ZoomUpTextColour   = OnButtonTextColour
            ZoomUpButtonColour = OnButtonColour
        else:
            ZoomUpTextColour   = OffButtonTextColour
            ZoomUpButtonColour = OffButtonColour

        if zoom > 1:
            ZoomDownTextColour   = OnButtonTextColour
            ZoomDownButtonColour = OnButtonColour
        else:
            ZoomDownTextColour   = OffButtonTextColour
            ZoomDownButtonColour = OffButtonColour
            


        
        #code in progress
        map = pygame.transform.scale(map, [round(MapSize[0] * zoom), round(MapSize[1] * zoom)])
        
        graphbutton = (pygame.font.SysFont('arial', 32)).render(' Make Graph ', True, GraphButtonTextColour, GraphButtonColour) #create the graph button ⓵
        undobutton  = (pygame.font.SysFont('arial', 25)).render(' Undo ', True, UndoButtonTextColour, UndoButtonColour)
        redobutton  = (pygame.font.SysFont('arial', 25)).render(' Redo ', True, RedoButtonTextColour, RedoButtonColour)
        savebutton  = (pygame.font.SysFont('arial', 40)).render(' Save ', True, SaveButtonTextColour, SaveButtonColour) #create the save button ⓵ 
        logoffbutton   = (pygame.font.SysFont('arial', 40)).render(' Logoff  ', True, LogoffButtonTextColour, LogoffButtonColour) #create the log off button ⓵
        zoomupbutton   = (pygame.font.SysFont('arial', 13)).render('    +    ', True, ZoomUpTextColour, ZoomUpButtonColour)
        zoomdownbutton = (pygame.font.SysFont('arial', 13)).render('    -    ', True, ZoomDownTextColour, ZoomDownButtonColour)
        zoompercentage = (pygame.font.SysFont('arial', 13)).render(str(str(int(zoom * 100)) + '%'), True, (0,0,0))
        performalgorithmbutton = (pygame.font.SysFont('arial', 32)).render(' Perform Algorithm ', True, PerformAlgorithmTextColour, PerformAlgorithmButtonColour) #⓵
        
        screen.blit(optionsbar, (0,0))
        screen.blit(optionstext, (20,20))
        screen.blit(map, MapToScreenOffset) # the map surface is blit to the screen, with offsets to account for panning, zooming and the Options bar
     

        mapbox = pygame.transform.scale(map, [192, 88]) # updated every loop, as the map surface can change
        
        pygame.draw.rect(mapbox, (0,0,100), pygame.Rect(-(MapToScreenOffset[0])/(8*zoom), -(MapToScreenOffset[1] - 100)/(8*zoom), 192/zoom, 88/zoom ), 2) #the legnths default are 192,88 
#same as map surface,but ÷ by zoom for the updated legnths
#another rectangle drawn onto the mapbox, The position is the inverted version of the Map to screen offset, so negative, and ÷ 8 because the actual map surface is that size relative  
        screen.blit(mapbox, MapBoxPosition) 
        screen.blit(graphbutton , GraphButtonPosition) #actually display the graph button on the screen ⓵
        screen.blit(undobutton  , UndoButtonPosition)
        screen.blit(redobutton  , RedoButtonPosition)
        screen.blit(savebutton  , SaveButtonPosition) #actually display the save button on the screen ⓵ 
        screen.blit(logoffbutton  , LogoffButtonPosition)#actually display the logoff button on the screen ⓵
        screen.blit(zoomtext, ZoomTextPosition)
        screen.blit(zoompercentage , ZoomPercentagePosition)
        screen.blit(zoomupbutton   , ZoomUpButtonPosition)
        screen.blit(zoomdownbutton , ZoomDownButtonPosition)
        screen.blit(performalgorithmbutton , PerformAlgorithmButtonPosition) #actually display the button on the screen ⓵
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #allows the closing of the window
                pygame.display.quit()
                a = account
                
                for each in dir():
                    if (each != a) and (each[0:2] != "__") and (each in globals()):
                        print(globals()[each])
                        del globals()[each]
                    
                displaying = False
                
                home_page()
            """
            if selectinggraph:
                
                found    = False
                SubGraph = None
                for EachGraph in SubGraphs:
 
                    if not found:
                        for n in range(0, len(EachGraph.keys()) -1):
                            if check_vertex((list(EachGraph.keys())[n], (list(EachGraph.keys())[n+1])),pygame.mouse.get_pos()):
                                SubGraph = EachGraph
                                found = True
                                break
                            elif (distance_between(list(EachGraph.keys())[n],pygame.mouse.get_pos()) <= 5) and (SubGraph == None):
                                SubGraph = EachGraph
            
            """  

            if event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL): 
                    ctrl = True 

                if selectinggraph:
                    if event.key == pygame.K_RETURN: #if enter pressed
                                                 
                        """ used for testing 
                        print('enter pressed')
                        """
                        return SubGraphs[S] #to the select graph method ⓾


                    if event.key == pygame.K_RIGHT: #if right arrow 
                        S += 1  #⓽

                    if event.key == pygame.K_LEFT: #if left arrow 
                        S -= 1  #⓽
                
                if selectinglines:
                    if event.key == pygame.K_RETURN: #select the current saved map, if enter pressed
                        """used for testing"""
                        print('Enter clicked')
                        """ """
                        return 


                    if event.key == pygame.K_RIGHT: #move onto the next saved map
                        """used for testing"""
                        print('Right arrow clicked')
                        """ """
                        return +1

                    if event.key == pygame.K_LEFT: #move onto the previous saved map
                        """used for testing"""
                        print('Left arrow clicked')
                        """ """
                        return -1

                if selectingnodes:
                    """used for testing
                    if ctrl:
                        print('ctrl')
                    """ 

                    if event.key == pygame.K_RETURN:#⓻
                                                 
                        """ used for testing 
                        print('enter pressed')
                        """
                        return Node


                    if event.key == pygame.K_RIGHT: #⓺
                        """used for testing
                        print('Right arrow clicked')
                        """ 
                        next = True

                    if event.key == pygame.K_LEFT: #⓺
                        """used for testing
                        print('Left arrow clicked')
                        """ 
                        prior = True

                if displayingalorithm: #⓶ 
                    if event.key == pygame.K_RETURN:
                            return True

                if event.key == pygame.K_ESCAPE:
                    zoom = 1
                    MapToScreenOffset = [0,100]

                if editing and (event.key == pygame.K_DELETE): #if the delete button is pressed and the mode is editing
                    Lines = []
                    linesexist = False
                    try: NewLine = [] #if it exists
                    except: pass

                    try: del mapobject #if it exists
                    except: pass

            if event.type == pygame.MOUSEBUTTONDOWN: #if click   
                
                if (event.button == 4) or (event.button == 5) and (zooming == False) and canzoom: #the mouse scroll ①
                    """used for testing
                    print('zoomed from: ', end = "")
                    print(pygame.mouse.get_pos())
                    """ 
                    initialzoom = zoom
                    zooming     = True

                    MouseToSurfaceOffset = [(pygame.mouse.get_pos()[0] - MapToScreenOffset[0]) , (pygame.mouse.get_pos()[1] - MapToScreenOffset[1])] #②
                    InitialOffset        = [MapToScreenOffset[0], MapToScreenOffset[1]]

                if event.button == 3: #the right click            

                    if canpan: #if panning is allowed in the mode running
                        panning         = True
                        InitialMousePos = pygame.mouse.get_pos() #Get the mouses screen position 
                        InitialOffset   = [MapToScreenOffset[0], MapToScreenOffset[1]] 
                
                if event.button == 1: #the left click    
                    """used for testing
                    print(pygame.mouse.get_pos())
                    """ 
                    if selectinggraph:
                        """used for testing
                        print('left click')
                        """
                        return SubGraphs[S]

                    if pressing(SaveButtonPosition, savebutton, pygame.mouse.get_pos()) and (SaveButtonColour ==  OnButtonColour): #⓸ 
                        #if the button is on and being pressed
                        Save(Lines)
                        #⓷  if pressing the button and it is on
                    if pressing(LogoffButtonPosition, logoffbutton, pygame.mouse.get_pos()) and (LogoffButtonColour ==  OnButtonColour):
                        pygame.display.quit()
                        del globals()['account'] #loging off
                        displaying = False
                        pygame.display.quit()
                        login() #⓸
                        home_page()
                        return

                    if pressing(GraphButtonPosition, graphbutton, pygame.mouse.get_pos()) and (GraphButtonColour ==  OnButtonColour): 	#if pressing graph button, if it is on ⓷
                        mapobject = map_class(Lines) #instantiate as map class

                        if ctrl: #if the user holds ctrl then endnodes won't be included
                            mapobject.make_graph(False) #⓸
                        elif not(ctrl):
                            mapobject.make_graph(True) #⓸

                        """used for testing
                        print("make_graph()")
                        """ 
                        """used for testing
                        print(mapobject.graph)
                        """
                    elif pressing(ZoomUpButtonPosition, zoomupbutton, pygame.mouse.get_pos()) and (ZoomUpButtonColour ==  OnButtonColour):
                        initialzoom = zoom
                        zooming     = True
                        zoomplus    = True

                        MouseToSurfaceOffset = [(768 - MapToScreenOffset[0]) , (450 - MapToScreenOffset[1])]
                        InitialOffset        = [MapToScreenOffset[0], MapToScreenOffset[1]]
                        
                        zoom += 0.25
                    elif pressing(ZoomUpButtonPosition, zoomupbutton, pygame.mouse.get_pos()): pass
                    elif pressing(ZoomDownButtonPosition, zoomdownbutton, pygame.mouse.get_pos()) and (ZoomDownButtonColour ==  OnButtonColour):
                        initialzoom = zoom
                        
                        MouseToSurfaceOffset = [(768 - MapToScreenOffset[0]) , (450 - MapToScreenOffset[1])]
                        InitialOffset        = [MapToScreenOffset[0], MapToScreenOffset[1]]
                        
                        zoom -= 0.25
                        
                        zoomduringzooming = zoom/initialzoom
                        MapToScreenOffset = [InitialOffset[0] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[0]) , InitialOffset[1] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[1])]
                        print(MapToScreenOffset)
                        if (MapToScreenOffset[0] + (zoom * 1536)) < 1536: MapToScreenOffset[0] += 1536 - ((zoom * 1536)+ MapToScreenOffset[0]) #problem 
                        if (MapToScreenOffset[1] + (zoom * 700)) < 800: MapToScreenOffset[1] += 800 - ((zoom * 700)+ MapToScreenOffset[1])     #problem
                        if MapToScreenOffset[0] > 0: MapToScreenOffset[0] = 0
                        if MapToScreenOffset[1] > 100: MapToScreenOffset[1] = 100

                        #print(MapToScreenOffset)
                    elif pressing(ZoomDownButtonPosition, zoomdownbutton, pygame.mouse.get_pos()): pass
                    elif (0 < round(pygame.mouse.get_pos()[0]) < 1536) and (100 < round(pygame.mouse.get_pos()[1]) < 800) and candraw:
                        drawing     = True
                        Point = [round((pygame.mouse.get_pos()[0] - MapToScreenOffset[0])/zoom), round((pygame.mouse.get_pos()[1] - MapToScreenOffset[1])/zoom)]
                        #this Point is based on the map surface of default size
                        NewLine = [[Point[0] , Point[1]]]

                        # if pressing the button and it is on   ⓸
                    if pressing(PerformAlgorithmButtonPosition, performalgorithmbutton, pygame.mouse.get_pos()) and (PerformAlgorithmButtonColour == OnButtonColour):
                        mapobject.perform_algorithm()  #E used for testing


                if event.button == 4 and zoom < 3: #zoom in
                    zoom += 0.25
                    """used for testing 
                    print('zoom: ' + str(zoom) + ' from ' +  str(pygame.mouse.get_pos())) 
                    """
                if event.button == 5 and zoom > 1: #zoom out
                    zoom -= 0.25
                    """used for testing 
                    print('zoom: ' + str(zoom) + ' from ' +  str(pygame.mouse.get_pos())) 
                    """
                if zooming == True:
                    zoomduringzooming = zoom/initialzoom
                    if (((InitialOffset[0] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[0])) <= 0) and ((InitialOffset[1] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[1])) <= 100) and
                            #constraints for map surface (relative to the screen): furthermost left, top, furthermost right, bottom
                          ((((InitialOffset[0] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[0])) + round(MapSize[0] * zoom)) >= 1536)
                     and  (((InitialOffset[1] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[1])) + round(MapSize[1] * zoom)) >= 800)) ):

                        MapToScreenOffset = [InitialOffset[0] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[0]) , InitialOffset[1] - ((zoomduringzooming - 1) * MouseToSurfaceOffset[1])]
                        #offset altered to account for the zooming
                    else:
                        zoom = initialzoom #if the contraints aren't fullfilled, then the zoom is canceled, and the offset according to what would have been is not carried out
                    
                    if zoomplus == True: 
                        zooming  = False
                        zoomplus = False

                """used for testing 
                if drawing:
                    Point = [round((pygame.mouse.get_pos()[0] - MapToScreenOffset[0])/zoom), round((pygame.mouse.get_pos()[1] - MapToScreenOffset[1])/zoom)]
                    #this Point is based on the map surface of default size

                    if "NewLine" in globals(): #if the NewLine hasn't been made yet it is created
                        k = 0 #constant to be tested, and changed depending on apparent results

                        if (abs(NewLine[len(NewLine) - 1][0] - Point[0]) > k) or (abs(NewLine[len(NewLine) - 1][1] - Point[1]) > k):
                            NewLine.append(Point)
                    else: #if the NewLine hasn't been made yet it is created
                        NewLine = [Point[0] , Point[1]]
                        print(NewLine)
                """
            if event.type == pygame.KEYUP: #if release key

                if (event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL): 
                    ctrl = False           

                if selectingnodes:  #⓺
                    if event.key == pygame.K_RIGHT:
                        """used for testing
                        print('Right arrow released')
                        """ 
                        next = False                        

                    if event.key == pygame.K_LEFT:
                        """used for testing
                        print('Left arrow released')
                        """ 
                        prior = False

            if event.type == pygame.MOUSEBUTTONUP: #if click released

                if  event.button == 3: #right click     ⑦
                    """used for testing
                    P[1] += MouseOffset[1]
                    print('Overall mouse offseting: ' + str(P)) #for testing 
                    """
                    panning = False

                if (event.button == 4) or (event.button == 5):
                    zooming = False

                if event.button == 1: #the left click  
                    if drawing == True:
                        drawing     = False
                        """used for testing
                        print(NewLine)
                        """
                        if len(NewLine) > 1: #a single coordinate is not valid as a line
                            Lines.append(NewLine)

                        """used for testing
                        print(Lines)
                        """
        
        if selectingnodes:
            if next == True:
                time.sleep(0.2)
                if ctrl or (coordinatenumber == (len(globals()['SubGraphLines'][linenumber])-1)): #if on the last coordinate on an edge
                    linenumber += 1
                    coordinatenumber = 0
                else:
                    coordinatenumber += 1
            if prior == True:
                time.sleep(0.2)
                if ctrl or (coordinatenumber == 0): #if on first coordinate on an edge
                    linenumber -= 1
                    linenumber = linenumber % len(globals()['SubGraphLines'])
                    coordinatenumber = (len(globals()['SubGraphLines'][linenumber])-1)
                else: 
                    coordinatenumber -= 1

        
        if panning:
            MouseOffset = [pygame.mouse.get_pos()[0] - InitialMousePos[0], pygame.mouse.get_pos()[1] - InitialMousePos[1]] #how much have panned
                                      #④             #⑤                                #④             #⑤
            """ used for testing
            if (MouseOffset[0]) != K:
                K = MouseOffset
                print('mouse offset: ' + str(MouseOffset[0])) 
            """

            if ((InitialOffset[0] + MouseOffset[0]) <= 0) and ((InitialOffset[0] + MouseOffset[0]) + round(MapSize[0] * zoom) >= 1536): #contraints
                MapToScreenOffset[0] = InitialOffset[0] + MouseOffset[0] #surface compared to screen #horizontal panning ⑥
            """ used for testing
            else: 
                print('contraints breached')
            """

            if ((InitialOffset[1] + MouseOffset[1]) <= 100) and ((InitialOffset[1] + MouseOffset[1]) + round(MapSize[1] * zoom) >= 800): #constraints
                MapToScreenOffset[1] = InitialOffset[1] + MouseOffset[1] #vertical panning ⑥
            """ used for testing
            else: 
                print('contraints breached')
            """

        if drawing:
            Point = [round((pygame.mouse.get_pos()[0] - MapToScreenOffset[0])/zoom), round((pygame.mouse.get_pos()[1] - MapToScreenOffset[1])/zoom)]
            #this Point is based on the map surface of default size
            k = 4 #constant to be tested, and changed depending on apparent results
            o = 4 #likewise as k
            # if the new point isn't identical to the one before, and the person is drawing within the screen
            if ((abs(NewLine[len(NewLine) - 1][0] - Point[0]) > k) or (abs(NewLine[len(NewLine) - 1][1] - Point[1]) > k)) and (0 < Point[0] < 1536) and (0 < Point[1] < 700):
                NewLine.append(Point)
            if pygame.mouse.get_pos()[1] <= 100:
                if (MapToScreenOffset[1] + o) <= 100:
                    MapToScreenOffset[1] += o 
                else:
                    pass
                    """ used for testing
                    print('MapToScreenOffset[1] + o: ' + str(MapToScreenOffset[1] + o))
                    print('o: ' + str(o))
                    """
                    
            elif pygame.mouse.get_pos()[1] >= 798: #decreased from 800
                if ((MapToScreenOffset[1] - o ) + round(MapSize[1] * zoom)) >= 798: #decreased from 800
                    MapToScreenOffset[1] -= o

            if pygame.mouse.get_pos()[0] == 0: 
                if (MapToScreenOffset[0] + o) <= 0:
                    MapToScreenOffset[0] += o 

            elif pygame.mouse.get_pos()[0] >= 1534:#decreased from 1536
                if ((MapToScreenOffset[0] - o) + round(MapSize[0] * zoom)) >= 1536:
                    MapToScreenOffset[0] -= o

def login():
    global loginpage
    loginpage = tk.Tk()
    loginpage.wm_title("New Account")  
    loginpage.geometry('1536x800')

    username  = StringVar()
    password  = StringVar() 

    ttk.Label(loginpage, text=' Log In ', font=("Verdana", 40)).pack(side="top", fill="x", pady=10) #title
    
    ttk.Label(loginpage, text=' Username ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(loginpage, width=50, font=('Arial 24'), textvariable = username).pack() #entry box with inputs assigned to username ⓵

    ttk.Label(loginpage, text=' Password ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(loginpage, width=50, font=('Arial 24'), textvariable = password, show="*" ).pack() #entry box with inputs assigned to password ⓶
    #button when pressed login function got with inputs as parameters
    Button(loginpage, text=" login ",  width=55, height=3,  command = lambda:[check_login(username.get(), password.get())]).pack(pady=30) #⓷

    loginpage.mainloop()
   
def check_login(username, password):

    userdirectory = os.path.join(os.getcwd(), str(username)) #if the account exists, the location of the directory

    Valid = True
    
    for char in[ '/', '"', "'", ':', ';','{','}','=','>','<',' ']: #unnecessary characters, which may be used in injection attacks ⓷ 
        if ( (char in username)  or   (char in password)):  Valid = False
        #if the directory exists
    if os.path.isdir(userdirectory) and (len(username) != 0) and (Valid == True): #if there is a directory with the username given ⓵ ⓶ 

        file = open(os.path.join(userdirectory, 'password.txt'), "r")
        h = file.read() #hash
        file.close()
        if md5hashing(password) == h: #if hashing the password = whats saved⓸ 
            global account #logged in  ⓹ 
            account = username
            popup = tk.Tk()
            popup.wm_title("") 
            ttk.Label(popup, text='Logged In successfully', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)       
            Button(popup, text="OK",  width=12 , command = lambda:[popup.destroy(), loginpage.destroy()]).pack(pady="5")
            return

    if Valid == False: cant_select('Faulty input') #if erroneous inputs
    else: cant_select('Invalid Credentials') #error messages

def new_account():
    global accountpage #so it is accessible by the Make account function
    accountpage = tk.Tk() #new window
    accountpage.wm_title("New Account")  
    accountpage.geometry('1536x800') #same size as mapping editor

    username  = StringVar()
    password  = StringVar()
    password2 = StringVar()
    email     = StringVar()

    ttk.Label(accountpage, text=' Make a New Account ', font=("Verdana", 40)).pack(side="top", fill="x", pady=10) #title at top of page
    
    ttk.Label(accountpage, text=' Username ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(accountpage, width=50, font=('Arial 24'), textvariable = username).pack() #entry box with inputs assigned to username ⓵ 

    ttk.Label(accountpage, text=' Password ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(accountpage, width=50, font=('Arial 24'), textvariable = password, show="*").pack()  #entry box with inputs visualised as asterisks ⓶ 

    ttk.Label(accountpage, text=' Re enter Password ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(accountpage, width=50, font=('Arial 24'), textvariable = password2, show="*").pack()  #entry box with inputs visualised as asterisks ⓷ 

    ttk.Label(accountpage, text=' Email ', font=("Verdana", 20)).pack(side="top", fill="x", pady=20, padx=310)
    ttk.Entry(accountpage, width=50, font=('Arial 24'), textvariable = email).pack() #entry box with inputs assigned to email ⓸ 

    Button(accountpage, text=" Register ",  width=55, height=3,  command = lambda:[Make_account(username.get(), password.get(), password2.get(), email.get())]).pack(pady=30) 
    #button which calls the make account function when pressed, with the inputs as parameters
    accountpage.mainloop()

def Make_account(username, password, password2, email):  
    """used for testing
    print(username)
    print(len(username))
    """ 
    Valid = True
    
    for char in[ '/', '"', "'", ':', ';','{','}','=','>','<',' ',',']:  #unnecessary characters, which may be used in injection attacks ⓷ 
        if ( (char in username)  or 
             (char in password)  or
             (char in password2) or 
             (char in email)   ):
           Valid = False
           print(char)

    
    if not Valid:   #⓷ 
        cant_select(' Faulty input ') #error message
        return

    elif password != password2: #⓶ 
        cant_select(' Passwords not Matching! ') #error message
        return

    elif len(username) < 4: #⓵ 

        cant_select(' username too short!\n Minimum 4 characters ') #error message
        return

    elif len(username) > 16: #⓵ 
        cant_select(' username too long!\n Maximum 16 characters ') #error message
        return
    elif len(password) < 8: #⓵ 
        cant_select(' Password too short!\n Minimum 8 characters ') #error message
        return

    elif len(password) > 16: #⓵ 
        cant_select(' Password too long!\n Maximum 16 characters ') #error message
        return
    
    elif ('@' not in email) and (len(email) != 0): #email isn't cumpolsory ⓹ 
        cant_select(' invalid email ') #error message
        return

    elif os.path.isdir(os.path.join(os.getcwd(), str(username))):  #check for username duplication ⓸ 
        cant_select(' Account with the same name already created ') #error message
        return

    else: #⓺ 
        userdirectory = os.path.join(os.getcwd(), str(username)) #creates a path, where the program is stores, 
        #with the name of the user
        os.mkdir(userdirectory) #create the new directory for the new account
        file = open(os.path.join(userdirectory, 'password.txt'), "w") #creates a file in the directory called password
        file.write(md5hashing(password)) #adds the hash of the password to it
        file.close()
        """used for testing"""
        print('account created')
        """ """
        accountpage.destroy() #gets rid of account page, making new account over

def  Access_saved_maps():
    userdirectory = os.path.join(os.getcwd(), str(account))
    GraphNames = []
    GraphsLines = [] #storing all the maps consecutively
    if os.path.exists(os.path.join(userdirectory, 'Lines.json')): #if there is a directory called lines
        filename = 'Lines.json'
        GraphNames.append(filename)
        f = open(os.path.join(userdirectory, filename), "r")
        GraphsLines.append(json.load(f))        #⓶ 
        f.close()
        
    for l in range(1,100): #assume not gonna have > 100 saved files, loop through all the files
        if os.path.exists(os.path.join(userdirectory, 'Lines[' + str(l) + '].json')): #if the file of that name exists
            filename = 'Lines[' + str(l) + '].json'
            GraphNames.append(filename)
            f = open(os.path.join(userdirectory, filename), "r")
            L = []
            GraphsLines.append(json.load(f))        #add the lines in the file to the list ⓶ 
            f.close()         
    #prompt to select map ⓵ 
    savepopup = tk.Tk()
    savepopup.wm_title("")
    savepopup.geometry('1536x800')
    ttk.Button(savepopup, text="    Select map     ", command = lambda:[savepopup.destroy()]).pack() #allow subgraph to be selected 
    ttk.Label(savepopup, text='Press enter to select it, and the left and right arrows to navigate', font=("Verdana", 20)).pack(side="top", fill="x", pady=10)       
    savepopup.mainloop()
    e = 0
    while True and len(GraphsLines) > 0: #⓷  
        s = display_mapping_editor(GraphsLines[e], (192,192,192), False, False, False, False, False, False, True)
        if   s == +1:   e += 1 #in order to go forward
        elif s == -1:   e -= 1 #in order to go back, as next loop will add 1
        else: 
            display_mapping_editor(GraphsLines[e]) #⓸ default editor mode
            break
        e = e % len(GraphsLines)

    



def home_page():

    try: 
        account  #see if account exists
        loggedin = True
    except: 
        loggedin = False

    #button information is uniform
    global OffButtonTextColour 
    global OffButtonColour     
    global OnButtonTextColour  
    global OnButtonColour      

    OffButtonTextColour = '#363232'      #dark grey
    OffButtonColour     = '#e3dcdc'      #light grey
    OnButtonTextColour  = '#000000'      #black
    OnButtonColour      = '#ffffff'      #white

    popup = tk.Tk()
    popup.wm_title("homepage")   
    popup.geometry('1536x800')
    ttk.Label(popup, text=' Home ', font=("Verdana", 40)).pack(side="top", pady=10) #title
    #buttons with functions called if pressed   
    Button(popup, text="          log in           ",  width=120, height=6, bg=OnButtonColour, command = lambda:[popup.destroy(),     login()  , home_page() ]).pack(pady="12") 
    Button(popup, text="    Make a new account     ",  width=120, height=6, bg=OnButtonColour, command = lambda:[popup.destroy(), new_account(), home_page() ]).pack(pady="12")

    if loggedin: #buttons off if not logged in
        Button(popup, text="      Create a new map         ",  width=120, height=6, bg=OnButtonColour, command = lambda:[popup.destroy(),      display_mapping_editor(), login(), home_page()]).pack(pady="5") #⓷ 
        Button(popup, text="     Edit an saved map         ",  width=120, height=6, bg=OnButtonColour, command = lambda:[popup.destroy(),        Access_saved_maps()     , home_page()]).pack(pady="5") #Access_saved_maps to be coded
    else: #⓸ 
        errormessage = 'Not logged in'
        Button(popup, text="      Create a new map         ",  width=120, height=6 , bg=OffButtonColour, command = lambda:[cant_select(errormessage)]).pack(pady="12") #⓷ 
        Button(popup, text="     Edit an saved map         ",  width=120, height=6 , bg=OffButtonColour, command = lambda:[cant_select(errormessage)]).pack(pady="12") #⓸ 

    popup.mainloop()
            
#a = check_vertex([[80,40],[100,20]],[[50,30],[130,50]])
#print(a)

"""used for testing
Lines = S
#test_map = map_class(Lines)
#print(test_map.graph)
#test_map.make_graph()
#print(test_map.graph)
display_mapping_editor(Lines)
""" 

while True:
    global GlobalVariables

    home_page()

"""used for testing"""
print('pressed ')
""" """