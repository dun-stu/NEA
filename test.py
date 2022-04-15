import pygame, sys
import time
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