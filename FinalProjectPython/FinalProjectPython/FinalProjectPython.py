#Python code for the final project for Math 475

import sys
import math


def FCN_NozzleShape(x):
    #Based on Equation 7.73 on p.307 of Anderson
    A = 1+ 2.2*(x-1.5)*(x-1.5)
    return A

def FCN_Veolocity(x):
    #Using equation 7.74 on p. 308 of Anderson
    #Assumes t=0
    row = 1- (0.3146*x)
    tao = 1 - (0.2314*x)
    v = (0.1 +(1.09*x))*(math.sqrt(tao))
    return row, tao, v

def calculateInterval(step,xMin, stepSize):
    value = xMin + (step*stepSize)
    return value

def CalculateTable(xMin,xMax,xSteps):
    print("xMin: " + str(xMin)+ " xMax: " + str(xMax) + " xSteps: " + str(xSteps))
    name = "debugFile_"+str(xSteps)+".txt"
    file = open(name,"w")
    file.write( 'n    xStep     A/A*     p/p0     V/a0    T/T0     \n')
    #initialize the values
    A = 0.0
    tao = 0.0
    row = 0.0
    V = 0.0
    xCurrent = xMin
    stepSize = (xMax-xMin)/xSteps
    for n in range(int(xSteps+1)):
        xCurrent = calculateInterval(n,xMin,stepSize)
        A = FCN_NozzleShape(xCurrent)
        row,tao, V = FCN_Veolocity(xCurrent)
        #Print out the values
        file.write(str(n) + " " + str(xCurrent) + " " + str(A)+ " " + str(row) + " " + str(V) + " " + str(tao) + "\n")
        print(str(n) + " " + str(xCurrent) + " " + str(A)+ " " + str(row) + " " + str(V) + " " + str(tao) + "\n")
    file.close

#Main body of the code

#Prompt the user for inputs
xMin = float(input("xMin = "))
xMax = float(input("xMax = "))
xSteps = int(input("xInterval = "))
xSteps = 30
xMin = 0
xMax = 3
CalculateTable(xMin,xMax,xSteps)