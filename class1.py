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

                """used for testing"""
            elif (m1 != m2):
                print('gradients not the same')
            
            """used for testing"""
        else:
            print('(third) coordinate outside coordinate ranges')
            """"""
        return False


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

    def get_connections(self):

        for EachNode in self.graph.keys():
            for EachLine in self.Lines:
                for v1 in range(0,len(EachLine)):
                    """used for testing
                    print('EachNode = ', end = "")
                    print(EachNode)
                    print('tuple(EachLine[v1]) = ', end = "")
                    print(tuple(EachLine[v1]))

                    """
                    if EachNode == check_vertex(): #tbc 
                        d = 0
                        nc = False
                        for v2 in range((v1-1), -1,-1):
                            
                            if nc == True:
                                continue

                            d += math.sqrt(((EachLine[v2][0] - EachLine[v2+1][0])**2) + ((EachLine[v2][1] - EachLine[v2+1][1])**2))
                            for EachVertex in self.Nodes:
                                if EachLine[v2] == EachVertex:
                                    self.graph[EachNode].append([EachLine[v2],d])
                                    nc = True
                                    continue
                        d = 0
                        nc = False
                        for v2 in range((v1+1), len(EachLine)):
                            
                            if nc == True:
                                continue

                            d += math.sqrt(((EachLine[v2][0] - EachLine[v2-1][0])**2) + ((EachLine[v2][1] - EachLine[v2-1][1])**2))
                            for EachVertex in self.Nodes:
                                if EachLine[v2] == EachVertex:
                                    self.graph[EachNode].append([Eachline[v2],d])
                                    nc = True
                                    continue

#comment what


    def make_graph(self):
        self.get_nodes()
        self.graph = {EachNode:[] for EachNode in self.Nodes}
      #  self.get_connections()

      
print(check_vertex(((8,6),(12,14)),(12,14)))

"""used for testing
Map_Instance = map([[[20,30],[50,30],[130,50],[110,70],[80,80],[70,70],[80,40],[100,20],[120,10]],[[30,50],[20,30],[40,10],[50,50],[20,30],[10,10]]])
Map_Instance.make_graph()
print(Map_Instance.graph)
print(Map_Instance.Nodes)
"""           


    


