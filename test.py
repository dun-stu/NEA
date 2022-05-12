import os
import tkinter as tk

a = tk.Tk()
g = []
test = 'garbage'
g.append(test)
g.append(a)
print(g)
a.destroy()
del test
print(g)
while True: pass
"""

import json

score=[ [[50,550], [100,600]], [[100,500], [100,600]], [[150,550], [100,600]], [[150,550], [200,500]], [[250,450], [200,500]], [[150,450], [200,500]], [[150,450], [200,400]], [[150,450], [50,400]], [[100,350], [50,400]], [[100,350], [50,300]], [[100,350], [150,300]], [[150,300],[100,250]], [[150,300],[200,250]], [[100,250],[150,200]]
        ,[ [486,204], [525,210], [650,200], [875,220], [995,215], [1117, 290]	], [	[624,99], [650,140], [750,150], [820,130], [870,150], [910, 260], [910, 265], [900,295], [850,320], [800,330], [760,345], [700, 335], [650,310], [600,280], [570,230], [580,80], [600, 50], [660,50], [750,15], [830,98], [850,150], [845,195] 	]	]


with open("file.json", 'w') as f:
    # indent=2 is not needed but makes the file human-readable 
    # if the data is nested
    json.dump(score, f, indent=2) 

with open("file.json", 'r') as f:
    score = json.load(f)


for each in score:
    print(each)



 

with open(os.path.join('C://Users/User/source/repos/NEA/Final Nea/Amal','Lines[1].txt'),'r') as f:

   L = f.read()
   print(L)
   print("L.split('[', 0)")
   print(L.split('[', 0))
   print("L[0].split('[', 0)")
   print(L[0].split('[', 0))

T = ['1','2']
for x in range(0,len(T)-1):
    print(x)



L = {1: ['x','y','z'], 
     2: [] ,
     3: [] ,
     4: [] ,
     5: [] }
L[1].pop()
print(L[1])
print(len(L))
for each in range(0,len(L)):
    print(each)
del L[3]
print(L)

class edge():

    def __init__(self, Key, value):
        self.node1    = Key
        self.node2    = value[0]
        self.distance = value[1]
    
global D
D = {
     (1,2): ['n2', 'n5'],
     'n2': [(1,2), 'n6'],
     'n3': ['n2', 'n4'],
     'n4': ['n3', 'n5'],
     'n5': ['n4', (1,2)],
     'n6': ['n2']
     }

def check_cycle(StartNode, NodeFrom, List):

    for EachConnection in D[StartNode]:
        if EachConnection != NodeFrom:
            if EachConnection in List:
                return True
            List.append(EachConnection)
            C = check_cycle(EachConnection, StartNode, List)
            if C == True: return True

    return False
print(list(D.keys())[0])
print(check_cycle((1,2),None,[(1,2)]))


t = time.time()
print(t)
time.sleep(2)
print(t)
print(time.time())
pygame.init()

array = [(1,9),(2,9),(3,9),(4,9),(6,9)]
b = array[0]
array[0] = (2,9)
print(array[0])
print(b)
def f2():
    print(array)

class tester:

    def __init__(self):
        pass

    def f1(self):
        global array
        array = [(1,9),(2,9),(3,9),(4,9),(6,9)]
        f2()


t = tester()

#t.f1()
"""