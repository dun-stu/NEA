import math 

def check_vertex(CoordinateSet1, CoordinateSet2): #to check if the lines between two sets of coordinates intersect
  
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
            return (round(x, 2),round(y, 2))
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

            if (m1 == m2) or (CoordinateSet2 == tuple(CoordinateSet1[0])) or (CoordinateSet2 == tuple(CoordinateSet1[1])):
                return True

                """used for testing
            elif (m1 != m2):
                print('gradients not the same')
                """
            """used for testing
        else:
            print('(third) coordinate outside coordinate ranges')
            """
        return False

def distance_between(Point1, Point2):
    return math.sqrt(((Point1[0] - Point2[0])**2) + ((Point1[1] - Point2[1])**2))

class map:
    
    def __init__(self, Lines):
        self.Lines = Lines
        self.Nodes = []
        self.graph = {}

    def get_nodes(self):
            """used for testing
            print(len(self.Lines))
            """
            for l in range(0, (len(self.Lines))):
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
                        for EachVertex in self.Nodes:
                            if check_vertex((EachLine[v1],EachNode), EachVertex):
                                d = distance_between(EachVertex, EachNode)
                                if d != 0:   
                                    nc = True
                                    self.graph[EachNode].append([EachVertex, round(d,2)])

                        #"""
                        d = distance_between(EachLine[v1], EachNode)
                        
                        for v2 in range((v1), 0,-1): #checks for connections chronologically prior in the list
                            
                            if nc == True: break #if connection prior found

                            for EachVertex in self.Nodes:
                                if check_vertex((EachLine[v2],EachLine[v2 - 1]),EachVertex):
                                    d += distance_between(EachLine[v2],EachVertex)
                                    if d != 0: #if the 
                                        self.graph[EachNode].append([EachVertex,round(d,2)])
                                        nc = True
                                        break  

                            else: d += distance_between(EachLine[v2],EachLine[v2 - 1])
                       
                        
                        nc = False
                       # """
                        for EachVertex in self.Nodes:
                            if check_vertex((EachLine[v1 + 1],EachNode), EachVertex):
                                d = distance_between(EachVertex, EachNode)
                                if d != 0:
                                    nc = True
                                    self.graph[EachNode].append([EachVertex, round(d,2)])
                        #"""
                        d = distance_between(EachLine[v1+1], EachNode)
                        for v2 in range((v1+1), (len(EachLine)-1)):
                            if nc == True: break

                            for EachVertex in self.Nodes:
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
                                    if d != 0:
                                        self.graph[EachNode].append([EachVertex,round(d,2)])
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


    def make_graph(self):
        self.get_nodes()
        self.graph = {EachNode:[] for EachNode in self.Nodes}
        self.get_connections()


      
#print(check_vertex(((5,14),(15,3)),(15,3)))

"""used for testing"""
Map_Instance = map([[[20,30],[50,30],[130,50],[110,70],[80,80],[70,70],[80,40],[100,20],[120,10]],[[30,50],[20,30],[40,10],[50,50],[20,30],[10,10]]])
Map_Instance.make_graph()
print(Map_Instance.graph)
#print(Map_Instance.Nodes)
""""""           


    


