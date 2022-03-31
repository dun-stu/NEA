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
                                    self.Nodes.append(Node)
    def get_connections(self):
        raise NotImplementedError("To be implimented")
        for EachNode in self.graph.keys():
            for EachLine in self.Lines:
                for v1 in range(0,EachLine):
                    if EachNode == EachLine[v1]: 
                        d = 0

#comment


    def Make_graph(self):
        self.graph = {EachNode:[] for EachNode in self.Nodes}
        self.get_connections()

            


    


