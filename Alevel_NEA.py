
import pygame, sys
import math
pygame.init()


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

class map_class:
    
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
        """used for testing"""
        print(self.graph)
        """"""


                                    
def pressing(buttonposition, button, mouseposition):
   if (buttonposition[0]) < mouseposition[0] < (buttonposition[0] + (button.get_rect()).width) and (buttonposition[1]) < mouseposition[1] < (buttonposition[1] + (button.get_rect()).height): return True
   else: return False   

def display_mapping_editor(colour): # to be changed to Map.colour when OOP is implimented + more parameters(like map, user)

  #  colour = Map.colour #to be implimented
    screen  = pygame.display.set_mode((1536,800))
    OffButtonTextColour = (54, 50, 50)
    OffButtonColour     = (227, 220, 220)
    OnButtonTextColour  = (0, 0, 0)
    OnButtonColour      = (255, 255, 255)
    optionsbar  = pygame.Surface((1536,100))
    optionsbar.fill(colour)
    optionstext = (pygame.font.SysFont('arial', 52)).render('OPTIONS', True, (0,0,0))
    MapSize = (1536, 700)
    map     = pygame.Surface(MapSize)
    map.fill((255,255,255))          # map only colour option is white, as this is clearest to draw on
    mapbox  = pygame.transform.scale(map, [192, 88])
    MapBoxPosition        = (1100,6)
    GraphButtonTextColour = OffButtonTextColour
    GraphButtonColour     = OffButtonColour
    GraphButtonPosition   = (550,10)
    UndoButtonTextColour  = OffButtonTextColour
    UndoButtonColour      = OffButtonColour
    UndoButtonPosition    = (1390,10)
    RedoButtonTextColour  = OffButtonTextColour
    RedoButtonColour      = OffButtonColour
    RedoButtonPosition    = (1460,10)
    zoomtext    = (pygame.font.SysFont('arial', 16)).render('      Zoom        ', True, (0,0,0)) 

    ZoomTextPosition = (1410,45)
    ZoomPercentagePosition    = (1440,70)
     
    ZoomUpTextColour    = OnButtonTextColour
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
    zoom       = 1
    linesexist = False

    
    """used for testing
    P = ['x value not relevant', 0] #test for panning
    K = [0,0] #test for panning 
    """
    Lines = []
    #all defaults

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
        
        if linesexist:
            GraphButtonTextColour =  OnButtonTextColour
            GraphButtonColour     =  OnButtonColour
        else:
            GraphButtonTextColour =  OffButtonTextColour #if there are no lines, a graph can't be made
            GraphButtonColour     =  OffButtonColour

        if zoom < 3:
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
        graphbutton = (pygame.font.SysFont('arial', 32)).render('Make Graph', True, GraphButtonTextColour, GraphButtonColour)
        undobutton  = (pygame.font.SysFont('arial', 25)).render(' Undo ', True, UndoButtonTextColour, UndoButtonColour)
        redobutton  = (pygame.font.SysFont('arial', 25)).render(' Redo ', True, RedoButtonTextColour, RedoButtonColour)
        zoomupbutton   = (pygame.font.SysFont('arial', 13)).render('    +    ', True, ZoomUpTextColour, ZoomUpButtonColour)
        zoomdownbutton = (pygame.font.SysFont('arial', 13)).render('    -    ', True, ZoomDownTextColour, ZoomDownButtonColour)
        zoompercentage = (pygame.font.SysFont('arial', 13)).render(str(str(int(zoom * 100)) + '%'), True, (0,0,0))

        screen.blit(map, MapToScreenOffset) # the map surface is blit to the screen, with offsets to account for panning, zooming and the Options bar
        screen.blit(optionsbar, (0,0))
        mapbox = pygame.transform.scale(map, [192, 88])
        screen.blit(optionstext, (20,20))
        pygame.draw.rect(mapbox, (0,0,100), pygame.Rect(-(MapToScreenOffset[0])/(8*zoom), -(MapToScreenOffset[1] - 100)/(8*zoom), 192/zoom, 88/zoom ), 2)
        screen.blit(mapbox, MapBoxPosition) 
        screen.blit(graphbutton , GraphButtonPosition)
        screen.blit(undobutton , UndoButtonPosition)
        screen.blit(redobutton , RedoButtonPosition)
        screen.blit(zoomtext , ZoomTextPosition)
        screen.blit(zoompercentage , ZoomPercentagePosition)
        screen.blit(zoomupbutton , ZoomUpButtonPosition)
        screen.blit(zoomdownbutton , ZoomDownButtonPosition)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #allows the closing of the window
                displaying = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    zoom = 1
                    MapToScreenOffset = [0,100]

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 3: #the right click
                    panning         = True
                    InitialMousePos = pygame.mouse.get_pos()
                    InitialOffset   = [MapToScreenOffset[0], MapToScreenOffset[1]]


                if (event.button == 4) or (event.button == 5) and (zooming == False): #the mouse scroll
                    initialzoom = zoom
                    zooming     = True

                    MouseToSurfaceOffset = [(pygame.mouse.get_pos()[0] - MapToScreenOffset[0]) , (pygame.mouse.get_pos()[1] - MapToScreenOffset[1])]
                    InitialOffset        = [MapToScreenOffset[0], MapToScreenOffset[1]]

                if event.button == 1: #the left click
                    if pressing(GraphButtonPosition, graphbutton, pygame.mouse.get_pos()) and (GraphButtonColour ==  OnButtonColour):
                        mapobject = map_class(Lines)
                        mapobject.make_graph()
                        """used for testing"""
                        print("make_graph()")
                        """"""
                        pass
                    else:
                        drawing     = True
                        Point = [round((pygame.mouse.get_pos()[0] - MapToScreenOffset[0])/zoom), round((pygame.mouse.get_pos()[1] - MapToScreenOffset[1])/zoom)]
                        #this Point is based on the map surface of default size
                        NewLine = [[Point[0] , Point[1]]]

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
                        

            if event.type == pygame.MOUSEBUTTONUP:

                if  event.button == 3:
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
                        """used for testing"""
                        #print(NewLine)
                        """"""
                        if len(NewLine) > 1: #a single coordinate is not valid as a line
                            Lines.append(NewLine)
                        """used for testing
                        print(Lines)
                        """
                    

        if panning:
            MouseOffset = [pygame.mouse.get_pos()[0] - InitialMousePos[0], pygame.mouse.get_pos()[1] - InitialMousePos[1]] #how much have panned
            
            """ used for testing
            if (MouseOffset[0]) != K:
                K = MouseOffset
                print('mouse offset: ' + str(MouseOffset[0])) 
            """

            if ((InitialOffset[0] + MouseOffset[0]) <= 0) and ((InitialOffset[0] + MouseOffset[0]) + round(MapSize[0] * zoom) >= 1536): #contraints
                MapToScreenOffset[0] = InitialOffset[0] + MouseOffset[0] #surface compared to screen #horizontal panning
            """ used for testing
            else: 
                print('contraints breached')
            """

            if ((InitialOffset[1] + MouseOffset[1]) <= 100) and ((InitialOffset[1] + MouseOffset[1]) + round(MapSize[1] * zoom) >= 800): #constraints
                MapToScreenOffset[1] = InitialOffset[1] + MouseOffset[1] #vertical panning
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
                if (MapToScreenOffset[0] + o) <= 100:
                    MapToScreenOffset[0] += o 

            elif pygame.mouse.get_pos()[0] >= 1534:#decreased from 1536
                if ((MapToScreenOffset[0] - o) + round(MapSize[0] * zoom)) >= 1536:
                    MapToScreenOffset[0] -= o
                    
            
            
#a = check_vertex([[80,40],[100,20]],[[50,30],[130,50]])
#print(a)

"""used for testing
Lines = [[[20,30],[50,30],[130,50],[110,70],[80,80],[70,70],[80,40],[100,20],[120,10]],[[30,50],[20,30],[40,10],[50,50],[20,30],[10,10]]]
print(get_nodes(Lines))
"""



colour = (192,192,192)

display_mapping_editor(colour)
