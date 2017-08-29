from helpful import *

from random import randint

for i in range(10000):
    (a, b, c, d) = randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)
    if a < b:
        continue
    x = Climate.classify(a, b, c, d)
    if x == -999:
        quit(1)
    print("NICE!")