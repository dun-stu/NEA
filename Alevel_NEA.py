
import pygame, sys
import math


pygame.init()

def check_vertex(CoordinateSet1, CoordinateSet2): #trace table needed, appears not to work
    x1_1 = CoordinateSet1[0][0]
    x1_2 = CoordinateSet1[1][0]
    y1_1 = CoordinateSet1[0][1]
    y1_2 = CoordinateSet1[1][1]

    x2_1 = CoordinateSet2[0][0]
    x2_2 = CoordinateSet2[1][0]
    y2_1 = CoordinateSet2[0][1]
    y2_2 = CoordinateSet2[1][1]
    #zero error to be dealt with
    try:
        m1 = (y1_2 - y1_1)/(x1_2 - x1_1)
    except ZeroDivisionError:
        m1 = math.inf

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
        return [round(x, 2),round(y, 2)]
    else:
        """used for testing
        print('intersections outside coordinate ranges')
        """
        return False

def get_nodes(Lines):
            Nodes = []
            """used for testing
            print(len(Lines))
            """
            for l in range(0, (len(Lines))):
                for c in range(0, (len(Lines[l])-1)):
                    for l2 in range(l, (len(Lines))):
                        if l2 == l:
                            c1 = c
                        else:
                            c1 = 0
                        for c2 in range(c1, (len(Lines[l2])-1)):
                            Node = check_vertex([Lines[l][c],Lines[l][c+1]],[Lines[l2][c2],Lines[l2][c2+1]])

                            if Node == False:
                                pass
                            elif (Lines[l][c+1] == Lines[l2][c2]) and (l2 == l):
                                pass
                            
                            else:
                                for eachvertex in Nodes:
                                    if Node == eachvertex:
                                        Node = False

                                """used for testing
                                print([Lines[l][c],Lines[l][c+1]],[Lines[l2][c2],Lines[l2][c2+1]])
                                """
                                if Node == False:
                                    pass
                                else:
                                    Nodes.append(Node)
            return Nodes
                                    
    

def display_mapping_editor(colour): # to be changed to Map.colour when OOP is implimented + more parameters(like map, user)

  #  colour = Map.colour #to be implimented
    screen     = pygame.display.set_mode((1536,800))

    optionsbar = pygame.Surface((1536,100))
    optionsbar.fill(colour)
    MapSize = (1536, 700)
    map = pygame.Surface(MapSize)
    map.fill((255,255,255))          # map only colour option is white, as this is clearest to draw on
    mapbox = pygame.transform.scale(map, [192, 88])
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
            for EachLine in Lines:
                pygame.draw.lines(map, colour, False ,EachLine, width = 5)

            pygame.draw.lines(map, colour, False ,NewLine, width = 5) #if the NewLine hasn't been made yet, then this can't be run 

        except:
            pass


        #code in progress
        map = pygame.transform.scale(map, [round(MapSize[0] * zoom), round(MapSize[1] * zoom)])

        screen.blit(map, MapToScreenOffset) # the map surface is blit to the screen, with offsets to account for panning, zooming and the Options bar
        screen.blit(optionsbar, (0,0))
        mapbox = pygame.transform.scale(map, [192, 88])
        pygame.draw.rect(mapbox, (0,0,100), pygame.Rect(-(MapToScreenOffset[0])/(8*zoom), -(MapToScreenOffset[1] - 100)/(8*zoom), 192/zoom, 88/zoom ), 2)
        screen.blit(mapbox, (1100,6)) 
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
                    drawing     = False
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
                    
            
            
a = check_vertex([[80,40],[100,20]],[[50,30],[130,50]])
print(a)

"""used for testing"""
Lines = [[[20,30],[50,30],[130,50],[110,70],[80,80],[70,70],[80,40],[100,20],[120,10]],[[30,50],[20,30],[40,10],[50,50],[20,30],[10,10]]]
print(get_nodes(Lines))
""""""



colour = (192,192,192)

display_mapping_editor(colour)
