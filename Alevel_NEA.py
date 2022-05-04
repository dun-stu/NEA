
import pygame, sys
import math
import random
import time
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

def check_vertex(CoordinateSet1, CoordinateSet2, Version = 1): #to check if the lines between two sets of coordinates intersect
  
    x1_1 = CoordinateSet1[0][0]
    x1_2 = CoordinateSet1[1][0]
    y1_1 = CoordinateSet1[0][1]
    y1_2 = CoordinateSet1[1][1]

    try:
        m1 = (y1_2 - y1_1)/(x1_2 - x1_1)
    except ZeroDivisionError:
        m1 = math.inf

    if isinstance(CoordinateSet2[0], list):
        x2_1 = CoordinateSet2[0][0]
        x2_2 = CoordinateSet2[1][0]
        y2_1 = CoordinateSet2[0][1]
        y2_2 = CoordinateSet2[1][1]
        #zero error to be dealt with


        try:
            m2 = (y2_2 - y2_1)/(x2_2 - x2_1)
        except ZeroDivisionError:
            m2 = math.inf
    
        if m1 == m2:
            """used for testing
            print('gradients the same') 
            """
            return False

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
            return (x,y) #unrounded
        else:
            """used for testing
            print('intersections outside coordinate ranges')
            """
            return False
    elif isinstance(CoordinateSet2[0], float) or isinstance(CoordinateSet2[0], int): #to check if a third coordinate is between two #to be tested
        if (min(x1_1,x1_2) <= CoordinateSet2[0] <= max(x1_1,x1_2)) and ((min(y1_1,y1_2) <= CoordinateSet2[1] <= max(y1_1,y1_2))):
            #if the third coordinate is between the other two coordinates
            try:
                m2 = (CoordinateSet2[1] - y1_1)/(CoordinateSet2[0] - x1_1)
            except ZeroDivisionError:
                m2 = math.inf

            if (round(m1, 4) == round(m2, 4)) or (CoordinateSet2 == tuple(CoordinateSet1[0])) or (CoordinateSet2 == tuple(CoordinateSet1[1])): #dodgy 
                return True

                """used for testing"""
            elif (m1 != m2):
                print('m1 = ', end = "")
                print(m1)
                print('m2 = ', end = "")
                print(m2)
                """ """
            """used for testing
        else:
            print('(third) coordinate outside coordinate ranges')
            """
        return False

def distance_between(Point1, Point2):
    return math.sqrt(((Point1[0] - Point2[0])**2) + ((Point1[1] - Point2[1])**2))

class edge():

    def __init__(self, Key, value):
        self.node1    = Key
        self.node2    = value[0]
        self.distance = value[1]
 
class map_class:
    
    def __init__(self, Lines):
        self.Lines  = Lines
        self.Nodes  = []
        self.graph  = {}
        self.colour = (192,192,192)

    def get_nodes(self, endnodes):
            """used for testing
            print(len(self.Lines))
            """
            for l in range(0, (len(self.Lines))):
                if endnodes:
                    self.Nodes.append(tuple(self.Lines[l][0]))
                    self.Nodes.append(tuple(self.Lines[l][len(self.Lines[l])- 1]))
                for c in range(0, (len(self.Lines[l])-1)):
                    for l2 in range(l, (len(self.Lines))):
                        if l2 == l:
                            c1 = c
                        else:
                            c1 = 0
                        for c2 in range(c1, (len(self.Lines[l2])-1)):
                            Node = check_vertex([self.Lines[l][c],self.Lines[l][c+1]],[self.Lines[l2][c2],self.Lines[l2][c2+1]])

                            if Node == False:
                                pass
                            elif (self.Lines[l][c+1] == self.Lines[l2][c2]) and (l2 == l):
                                pass
                            
                            else:
                                for EachVertex in self.Nodes:
                                    if Node == EachVertex:
                                        Node = False

                                """used for testing
                                print([self.Lines[l][c],self.Lines[l][c+1]],[self.Lines[l2][c2],self.Lines[l2][c2+1]])
                                """
                                if Node == False:
                                    pass
                                else:
                                    Node = tuple(Node)
                                    self.Nodes.append(Node)

    def get_connections(self): #to be fixed 

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
                    if check_vertex((EachLine[v1],EachLine[v1 + 1]),EachNode): #v1 + 1 index is why v1 is in range len(Eachline) but -1
                        """used for testing
                        print(EachNode, end = "")
                        print(" found")
                        print('tuple(EachLine[v1]) = ', end = "")
                        print(tuple(EachLine[v1]))
                        print('tuple(EachLine[v1 + 1]) = ', end = "")
                        print(tuple(EachLine[v1 + 1]))
                        """ 
                       
                        nc = False
                        
                       # """
                        for EachVertex in self.graph.keys():
                            """used for testing
                            print(EachVertex)
                            """ 
                            if check_vertex((EachLine[v1],EachNode), EachVertex):
                                d = distance_between(EachVertex, EachNode)
                                if round(d,1) != 0:   
                                    nc = True
                                    self.graph[EachNode].append([EachVertex, round(d,6)])
                        
                        #"""
                        d = distance_between(EachLine[v1], EachNode)
                        
                        for v2 in range((v1), 0,-1): #checks for connections chronologically prior in the list
                            
                            if nc == True: break #if connection prior found

                            for EachVertex in self.graph.keys():
                                if check_vertex((EachLine[v2],EachLine[v2 - 1]),EachVertex):
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0: #if the 
                                        self.graph[EachNode].append([EachVertex,round(d,6)])
                                        nc = True
                                        break  

                            else: d += distance_between(EachLine[v2],EachLine[v2 - 1])
                       
                        
                        nc = False
                       # """
                        for EachVertex in self.graph.keys():
                            if check_vertex((EachLine[v1+1],EachNode), EachVertex):
                                d = distance_between(EachVertex, EachNode)
                                if round(d,1) != 0:
                                    nc = True
                                    self.graph[EachNode].append([EachVertex, round(d,6)])
                        #"""
                        d = distance_between(EachLine[v1+1], EachNode)
                        for v2 in range((v1+1), (len(EachLine)-1)):
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
                                d += distance_between(EachLine[v2],EachLine[v2 + 1])
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
            
#comment what


    def make_graph(self, endnodes = True):
        self.get_nodes(endnodes)
        self.graph = {EachNode:[] for EachNode in self.Nodes}
        self.get_connections()

        InitKeys = {key: self.graph[key] for key in self.graph.keys()}

        for EachKey in InitKeys: #rounding all the nodes
            self.graph[(round(EachKey[0], 6), round(EachKey[1], 6))] = self.graph.pop(EachKey)
        
        del InitKeys

        for EachValue in self.graph: #rounding all the connections
            """used for testing
            print(self.graph[EachValue])
            """
            for ec in range(0, len(self.graph[EachValue])):
                self.graph[EachValue][ec][0] = (round(self.graph[EachValue][ec][0][0], 6), round(self.graph[EachValue][ec][0][1], 6) )



    def select_graph(self):
        global SubGraphs
        SubGraphs = [] #has all the subgraphs in a list
        ToBeFound = [] 
        for EachNode in self.graph.keys(): #add all the nodes in a list
            ToBeFound.append(EachNode) #to be found

        while len(ToBeFound) != 0: #graph still needs traversing if there are still nodes to be found
            subgraph = {}
            queue = [ToBeFound[0]] #starting vertex for traversal
            while len(queue) != 0:
                for EachConnection in self.graph[queue[0]]: #goes through each of the connections to a node
                    if (EachConnection[0] in ToBeFound) and (EachConnection[0] not in queue):
                        queue.append(EachConnection[0]) #adds connections to the node, so they themselves can be checked for their connections

                ToBeFound.remove(queue[0]) #the node has been found and checked for connections
                subgraph.update({queue[0]:self.graph[queue[0]]}) #the node is part of the same subgraph as the rest in the iteration, as they are only added to the queue in the first place as they connect another node
                queue.pop(0) #so the next node in the list can be checked
            
            SubGraphs.append(subgraph)

        return display_mapping_editor(self.Lines,self.colour, False, False, True)

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
        MST.update({Edges[random.randint(0,(len(Edges) - 1))].node1: ''}) #choose a random start node
        while (edges < (len(subgraph.keys()) - 1)): #while num of edges < num of nodes - 1
            for EachEdge in Edges:
                if (EachEdge.node1 in MST.keys()) ^ (EachEdge.node2 in MST.keys()): #XOR, so the smallest Edge, which conects and unvisited node(not in MST) to the MST is added
                    #adding the edges to the minimum spanning tree (as a dictionary)
                    try:    MST[EachEdge.node1].append([EachEdge.node2, EachEdge.distance])     #if the node has been added already  
                    except: MST.update({EachEdge.node1: [[EachEdge.node2, EachEdge.distance]]}) #if the node is not part of the spanning tree yet

                    try:    MST[EachEdge.node2].append([EachEdge.node1, EachEdge.distance]) 
                    except: MST.update({EachEdge.node2: [[EachEdge.node1, EachEdge.distance]]})  
                    edges += 1
                    """used for testing"""
                    global SubGraphLines
                    SubGraphLines = self.get_algorithm_lines(subgraph, MST)
                    display_mapping_editor(self.Lines, self.colour, False, False, False, False, True) #so the additions are made incrementally on the screen
                    """ """
                    break
        return MST

    def kruscals(self, subgraph):
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
        edgenumber   = 0
        edges = 0
        while (edges < (len(subgraph.keys()) - 1)): #while num of edges < num of nodes - 1

            #adding the edges to the minimum spanning tree (as a dictionary)
            try:    MST[Edges[edgenumber].node1].append([Edges[edgenumber].node2, Edges[edgenumber].distance])     #if the node has been added already  
            except: MST.update({Edges[edgenumber].node1: [[Edges[edgenumber].node2, Edges[edgenumber].distance]]}) #if the node is not part of the spanning tree yet

            try:    MST[Edges[edgenumber].node2].append([Edges[edgenumber].node1, Edges[edgenumber].distance]) 
            except: MST.update({Edges[edgenumber].node2: [[Edges[edgenumber].node1, Edges[edgenumber].distance]]})

            """used for testing
            print(MST)
            """ 
            if check_cycle([Edges[edgenumber].node2, Edges[edgenumber].distance], None, [[Edges[edgenumber].node2, Edges[edgenumber].distance]], MST):
                MST[Edges[edgenumber].node1].pop()
                MST[Edges[edgenumber].node2].pop()
                if len(MST[Edges[edgenumber].node1]) == 0: del MST[Edges[edgenumber].node1]
                if len(MST[Edges[edgenumber].node2]) == 0: del MST[Edges[edgenumber].node2]
            else: 
                edges += 1
                """used for testing"""
                global SubGraphLines
                SubGraphLines = self.get_algorithm_lines(subgraph, MST)
                display_mapping_editor(self.Lines, self.colour, False, False, False, False, True)
                """ """
            edgenumber += 1
        return MST

    def perform_algorithm(self):

        subgraph = self.select_graph()
        
        global SubGraphs
        del SubGraphs
        C = check_cycle(list(subgraph.values())[0][0], None, [list(subgraph.values())[0][0]], subgraph)
        
        """E used for testing
        print(C)
        return E

        algorithm = display_mapping_editor(self.Lines, self.colour, False, False, False, True)
        if algorithm = 'KRUSCAL'S': 
            algorithmgraph = self.Kruscals(subgraph)

        etc
        """
        """used for testing"""
        #choice to be made, for initial testing Kruscals is used
        algorithmgraph = self.kruscals(subgraph) #algorithm to be created
        print('subgraph  ', end="")
        print(subgraph)
        print('algorithm graph   ', end="")
        print(algorithmgraph)
        #breakpoint()
        """ """
        global SubGraphLines
        SubGraphLines = self.get_algorithm_lines(subgraph, algorithmgraph)
        """used for testing
        print(SubGraphLines)
        breakpoint()
        """ 
        display_mapping_editor(self.Lines, self.colour, False, False, False, False, True)
        del SubGraphLines

    def get_algorithm_lines(self, subgraph, algorithmgraph):
        AlgorithmGraphLines = []
        for EachKey in algorithmgraph.keys(): 

            for EachLine in self.Lines: #possibly add Subgraphlines instead
                for v1 in range(0, (len(EachLine)-1)):
                   if check_vertex((EachLine[v1],  EachLine[v1 + 1]), EachKey):
                        """used for testing"""
                        print('EachKey:      ', end="")
                        print(EachKey)

                        """ """
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
                        """used for testing"""
                        print('EachLine:  ', end ="")
                        print(EachLine)
                        """ """
                        for v2 in range((v1+1), (len(EachLine)-1)):
                            if nc == True: break
                            Line.append(EachLine[v2])

                            for EachVertex in subgraph.keys():
                                if nc == True: break
                                if check_vertex((EachLine[v2],EachLine[v2 + 1]),EachVertex):
                                    """used for testing"""
                                    print('tuple(EachLine[v2]) = ', end = "")
                                    print(tuple(EachLine[v2]))
                                    print('tuple(EachLine[v2 + 1]) = ', end = "")
                                    print(tuple(EachLine[v2 + 1]))
                                    print('EachVertex = ' ,end = "")
                                    print(EachVertex)
                                    """ """
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0:
                                        nc = True

                                        for EachValue in algorithmgraph[EachKey]:
                                            """used for testing"""
                                            print('[EachVertex, round(d,6)]:    ', end="")
                                            print([EachVertex, round(d,6)])
                                            print('EachValue:    ', end="")
                                            print(EachValue)
                                            """ """
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
                                    """used for testing"""
                                    print('tuple(EachLine[v2]) = ', end = "")
                                    print(tuple(EachLine[v2]))
                                    print('tuple(EachLine[v2 - 1]) = ', end = "")
                                    print(tuple(EachLine[v2 - 1]))
                                    print('EachVertex = ' ,end = "")
                                    print(EachVertex)
                                    """ """
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if round(d,1) != 0:
                                        
                                        nc = True
                                        for EachValue in algorithmgraph[EachKey]:
                                            """used for testing"""
                                            print('[EachVertex, round(d,6)]:    ', end="")
                                            print([EachVertex, round(d,6)])
                                            print('EachValue:    ', end="")
                                            print(EachValue)
                                            """ """
                                            EachValue[1] = round(EachValue[1], 2)
                                            if [EachVertex, round(d,2)] == EachValue:  
                                                Line.append(EachVertex)
                                                AlgorithmGraphLines.append(Line)
                                                """used for testing"""
                                                print('[EachVertex, round(d,6)]:    ', end="")
                                                print([EachVertex, round(d,6)])
                                                """ """
                                                break

                            else: 
                                
                                d += distance_between(EachLine[v2],EachLine[v2 - 1])
                                """used for testing
                                print(d)
                                """  
                        #breakpoint()
                        
        return AlgorithmGraphLines 
        

def pressing(buttonposition, button, mouseposition):
   if (buttonposition[0]) < mouseposition[0] < (buttonposition[0] + (button.get_rect()).width) and (buttonposition[1]) < mouseposition[1] < (buttonposition[1] + (button.get_rect()).height): return True
   else: return False   


def display_mapping_editor(Lines = [], colour = (192,192,192), 
                           editing = True, makinggraph = False, 
                           selectinggraph = False, selectingalgorithm = False, 
                           displayingalorithm = False): 

    #Editor is a function with different modes
    
    #pygame.time.Clock().tick(100)

    #Varying functionality allowed depending on the mode
    if makinggraph:
        mgbutton = False #make graph button
        canpan   = True
        canzoom  = True
        candraw  = False
        pabutton = False #perform algorithm button

    if selectingalgorithm or selectinggraph or displayingalorithm:
        mgbutton = False #make graph button
        canpan   = False
        canzoom  = False
        candraw  = False
        pabutton = False #perform algorithm button

    if editing:
        mgbutton = True
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

    mapbox  = pygame.transform.scale(map, [192, 88])
    MapBoxPosition        = (1100,6)
    #A small image showing the whole drawing surface for positional awareness during panning/zooming

    #button information
    OffButtonTextColour = (54, 50, 50)
    OffButtonColour     = (227, 220, 220)
    OnButtonTextColour  = (0, 0, 0)
    OnButtonColour      = (255, 255, 255)

    #defaults for the buttons
    GraphButtonTextColour = OffButtonTextColour
    GraphButtonColour     = OffButtonColour
    GraphButtonPosition   = (550,10)

    UndoButtonTextColour  = OffButtonTextColour
    UndoButtonColour      = OffButtonColour
    UndoButtonPosition    = (1390,10)

    RedoButtonTextColour  = OffButtonTextColour
    RedoButtonColour      = OffButtonColour
    RedoButtonPosition    = (1460,10)

    PerformAlgorithmTextColour     = OffButtonTextColour
    PerformAlgorithmButtonColour   = OffButtonColour
    PerformAlgorithmButtonPosition = (510,55)

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

    """used for testing"""
    #Lines = [[[400, 300], [1200, 300]]]
    """ """
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

        if displayingalorithm:
            
            for EachLine in globals()['SubGraphLines']:
                pygame.draw.lines(map, (3, 123, 252) , False ,EachLine, width = 5)


                


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
            #print((time.time() - t))
            """
            if round(((time.time() - t) % 2),1) == 0:
                time.sleep(0.2)
                S += 1
            
            """
            S = S % len(SubGraphs)
            
            
            

            SubGraphLines = []
            
            for EachNode in list(SubGraphs[S].keys()):

                 for EachLine in Lines:
                     if ((max(EachLine[l][0] for l in range(0,len(EachLine))) >= EachNode[0] >= min(EachLine[l][0] for l in range(0,len(EachLine)))) and
                        (max(EachLine[l][1] for l in range(0,len(EachLine))) >= EachNode[1] >= min(EachLine[l][1] for l in range(0,len(EachLine))))):
                         for c in range(0, len(EachLine) - 1):
                             if check_vertex((EachLine[c], EachLine[c+1]), EachNode):
                                 if EachLine not in SubGraphLines: SubGraphLines.append(EachLine)


            for EachLine in SubGraphLines:
                 pygame.draw.lines(map, (3, 123, 252) , False ,EachLine, width = 5)

            for EachNode in SubGraphs[S].keys():
                pygame.draw.circle(map, (65, 250, 65), EachNode, 4) #to be changed
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
        if linesexist and mgbutton:
            GraphButtonTextColour =  OnButtonTextColour
            GraphButtonColour     =  OnButtonColour
        else:
            GraphButtonTextColour =  OffButtonTextColour #if there are no lines, a graph can't be made
            GraphButtonColour     =  OffButtonColour
        
        try:
            mapobject = mapobject #if the graph has been made yet
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
        
        graphbutton = (pygame.font.SysFont('arial', 32)).render(' Make Graph ', True, GraphButtonTextColour, GraphButtonColour)
        undobutton  = (pygame.font.SysFont('arial', 25)).render(' Undo ', True, UndoButtonTextColour, UndoButtonColour)
        redobutton  = (pygame.font.SysFont('arial', 25)).render(' Redo ', True, RedoButtonTextColour, RedoButtonColour)
        zoomupbutton   = (pygame.font.SysFont('arial', 13)).render('    +    ', True, ZoomUpTextColour, ZoomUpButtonColour)
        zoomdownbutton = (pygame.font.SysFont('arial', 13)).render('    -    ', True, ZoomDownTextColour, ZoomDownButtonColour)
        zoompercentage = (pygame.font.SysFont('arial', 13)).render(str(str(int(zoom * 100)) + '%'), True, (0,0,0))
        performalgorithmbutton = (pygame.font.SysFont('arial', 32)).render(' Perform Algorithm ', True, PerformAlgorithmTextColour, PerformAlgorithmButtonColour)

        screen.blit(map, MapToScreenOffset) # the map surface is blit to the screen, with offsets to account for panning, zooming and the Options bar
        screen.blit(optionsbar, (0,0))
        mapbox = pygame.transform.scale(map, [192, 88])
        screen.blit(optionstext, (20,20))
        pygame.draw.rect(mapbox, (0,0,100), pygame.Rect(-(MapToScreenOffset[0])/(8*zoom), -(MapToScreenOffset[1] - 100)/(8*zoom), 192/zoom, 88/zoom ), 2)
        screen.blit(mapbox, MapBoxPosition) 
        screen.blit(graphbutton , GraphButtonPosition)
        screen.blit(undobutton  , UndoButtonPosition)
        screen.blit(redobutton  , RedoButtonPosition)
        screen.blit(zoomtext, ZoomTextPosition)
        screen.blit(zoompercentage , ZoomPercentagePosition)
        screen.blit(zoomupbutton   , ZoomUpButtonPosition)
        screen.blit(zoomdownbutton , ZoomDownButtonPosition)
        screen.blit(performalgorithmbutton , PerformAlgorithmButtonPosition)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #allows the closing of the window
                displaying = False
                pygame.display.quit()
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
                if selectinggraph:
                    if event.key == pygame.K_RETURN:
                                                 
                        """ used for testing 
                        print('enter pressed')
                        """
                        return SubGraphs[S]


                    if event.key == pygame.K_RIGHT:
                        if selectinggraph:
                            t -= (time.time() - t) % 2
                            S += 1

                    if event.key == pygame.K_LEFT:
                        if selectinggraph:
                            t -= (time.time() - t) % 2
                            S -= 1

                if displayingalorithm:
                    if event.key == pygame.K_RETURN:
                            return True

                if event.key == pygame.K_ESCAPE:
                    zoom = 1
                    MapToScreenOffset = [0,100]

                if (event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL): 
                    ctrl = True 


            if event.type == pygame.MOUSEBUTTONDOWN: #if click   ①
                
                if (event.button == 4) or (event.button == 5) and (zooming == False) and canzoom: #the mouse scroll ①
                    """used for testing"""
                    print('zoomed from: ', end = "")
                    print(pygame.mouse.get_pos())
                    """ """
                    initialzoom = zoom
                    zooming     = True

                    MouseToSurfaceOffset = [(pygame.mouse.get_pos()[0] - MapToScreenOffset[0]) , (pygame.mouse.get_pos()[1] - MapToScreenOffset[1])] ②
                    InitialOffset        = [MapToScreenOffset[0], MapToScreenOffset[1]]

                if event.button == 3: #the right click            

                    if canpan: #if panning is allowed in the mode running
                        panning         = True
                        InitialMousePos = pygame.mouse.get_pos() #Get the mouses screen position 
                        InitialOffset   = [MapToScreenOffset[0], MapToScreenOffset[1]] #Initial mouse to screen offset ③


                
                if event.button == 1: #the left click
                    """used for testing
                    print(pygame.mouse.get_pos())
                    """ 
                    if selectinggraph:
                        """used for testing
                        print('left click')
                        """
                        return SubGraphs[S]




                    if pressing(GraphButtonPosition, graphbutton, pygame.mouse.get_pos()) and (GraphButtonColour ==  OnButtonColour):
                        mapobject = map_class(Lines)

                        if ctrl:
                            mapobject.make_graph(False)
                        elif not(ctrl):
                            mapobject.make_graph(True)

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

                    if pressing(PerformAlgorithmButtonPosition, performalgorithmbutton, pygame.mouse.get_pos()) and (PerformAlgorithmButtonColour == OnButtonColour):
                        E = mapobject.perform_algorithm()  #E used for testing
                        print('perform_algorithm()')

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
            if event.type == pygame.KEYUP:

                if (event.key == pygame.K_LCTRL) or (event.key == pygame.K_RCTRL): 
                    ctrl = False           


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
                    
            
            
#a = check_vertex([[80,40],[100,20]],[[50,30],[130,50]])
#print(a)

"""used for testing
Lines = [ [[50,550], [100,600]], [[100,500], [100,600]], [[150,550], [100,600]], [[150,550], [200,500]], [[250,450], [200,500]], [[150,450], [200,500]], [[150,450], [200,400]], [[150,450], [50,400]], [[100,350], [50,400]], [[100,350], [50,300]], [[100,350], [150,300]], [[150,300],[100,250]], [[150,300],[200,250]], [[100,250],[150,200]], [[200,250],[150,200]]
        ,[ [486,204], [525,210], [650,200], [875,220], [995,215], [1117, 290]	], [	[624,99], [650,140], [750,150], [820,130], [870,150], [910, 260], [910, 265], [900,295], [850,320], [800,330], [760,345], [700, 335], [650,310], [600,280], [570,230], [580,80], [600, 50], [660,50], [750,15], [830,98], [850,150], [845,195] 	]	]
#test_map = map_class(Lines)
#print(test_map.graph)
#test_map.make_graph()
#print(test_map.graph)
display_mapping_editor(Lines)
""" 


colour = (192,192,192)

display_mapping_editor()
