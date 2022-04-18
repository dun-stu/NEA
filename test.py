import pygame, sys
import time
import schedule

D = {
     (1,2): ['n2', 'n5'],
     'n2': [(1,2), 'n6'],
     'n3': ['n2', 'n4'],
     'n4': ['n3', 'n5'],
     'n5': ['n4', (1,2)],
     'n6': ['n2']
     }

def check_cycle(StartNode, NodeFrom, List, D):

    for EachConnection in D[StartNode]:
        if EachConnection != NodeFrom:
            if EachConnection in List:
                return True
            List.append(EachConnection)
            C = check_cycle(EachConnection, StartNode, List, D)
            if C == True: return True

    return False
print(list(D.keys())[0])
print(check_cycle((1,2),None,[(1,2)], D))

"""
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