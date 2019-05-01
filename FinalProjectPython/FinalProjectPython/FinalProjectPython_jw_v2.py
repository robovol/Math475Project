#Python code for the final project for Math 475

import math
import matplotlib.pyplot as plt

def FCN_NozzleShape(x):
    #Based on Equation 7.73 on p.307 of Anderson
    A = 1+ 2.2*(x-1.5)*(x-1.5)
    return A

def FCN_Veolocity(x):
    #Using equation 7.74 on p. 308 of Anderson
    #Assumes t=0
    row = 1 - (0.3146*x)
    tao = 1 - (0.2314*x)
    v = (0.1 +(1.09*x))*(math.sqrt(tao))
    return row, tao, v

def calculateInterval(step,xMin, stepSize):
    value = xMin + (step*stepSize)
    return value

def CalculateTable(xMin,xMax,xSteps):
    print("xMin: " + str(xMin) + " xMax: " + str(xMax) + " xSteps: " + str(xSteps))
    name = "debugFile_"+str(xSteps)+".txt"
    file = open(name,"w")
    file.write( 'n    xStep     A/A*     p/p0     V/a0    T/T0     \n')
    #initialize the values
    A = [0.0 for i in range(xSteps + 1)]
    T = [0.0 for i in range(xSteps + 1)]
    row = [0.0 for i in range(xSteps + 1)]
    V = [0.0 for i in range(xSteps + 1)]
    xCurrent = [0.0 for i in range(xSteps + 1)]
    stepSize = (xMax-xMin)/xSteps
    for n in range(int(xSteps + 1)):
        xCurrent[n] = calculateInterval(n, xMin, stepSize)
        A[n] = FCN_NozzleShape(xCurrent[n])
        row[n], T[n], V[n] = FCN_Veolocity(xCurrent[n])
        #Print out the values
#        file.write(str(n) + " " + str(xCurrent) + " " + str(A)+ " " + str(row) + " " + str(V) + " " + str(tao) + "\n")
#        print(str(n) + " " + str(xCurrent) + " " + str(A)+ " " + str(row) + " " + str(V) + " " + str(tao) + "\n")
        print(" %8d  %12.6f  %12.6f  %12.6f  %12.6f  %12.6f" % (n, xCurrent[n], A[n], row[n], V[n], T[n]))
#    print(" %8d  %12.6f  %12.6f  %12.6f  %12.6f  %12.6f" % (n, xCurrent[n], A[n], row[n], V[n], T[n]))
#    print("row = ", row)
    file.close
    return A, row, V, T

def timeStepping(A, T, row, V, timeSteps, xSteps, dx, index_for_graph):
    drow = [0.0 for i in range(xSteps + 1)]
    dV = [0.0 for i in range(xSteps + 1)]
    dT = [0.0 for i in range(xSteps + 1)]
    row_bar = [0.0 for i in range(xSteps + 1)]
    V_bar = [0.0 for i in range(xSteps + 1)]
    T_bar = [0.0 for i in range(xSteps + 1)]
    drow_bar = [0.0 for i in range(xSteps + 1)]
    dV_bar = [0.0 for i in range(xSteps + 1)]
    dT_bar =[0.0 for i in range(xSteps + 1)]
    drow_ave = [0.0 for i in range(xSteps + 1)]
    dV_ave = [0.0 for i in range(xSteps + 1)]
    dT_ave = [0.0 for i in range(xSteps + 1)]
    mach = [0.0 for i in range(xSteps + 1)]
    
    row_hist = [0.0 for i in range(timeSteps)]
    V_hist = [0.0 for i in range(timeSteps)]
    T_hist = [0.0 for i in range(timeSteps)]
    mach_hist = [0.0 for i in range(timeSteps)]
    
    for t in range(timeSteps):
        for i in range(xSteps):
            lamda = 1.4
            # equations 7.51 - 7.53
            drow[i] = - row[i] * (V[i + 1] - V[i])/dx - row[i] * V[i] * (math.log(A[i + 1]) - math.log(A[i]))/dx - V[i] * (row[i + 1] - row[i])/dx
            dV[i] = - V[i] * (V[i + 1] - V[i])/dx - 1/lamda * ((T[i + 1] - T[i])/dx + T[i]/row[i] * (row[i + 1] - row[i])/dx)
            dT[i] = - V[i] * (T[i + 1] - T[i])/dx - (lamda - 1) * T[i] * ((V[i + 1] - V[i])/dx + V[i] * (math.log(A[i + 1]) - math.log(A[i]))/dx)
            
            # equations 7.67 and 7.69
            a = math.sqrt(T[i])
            if i == 0:
                dt = .5 * dx/(a + V[i])
            else:
                dt = min(.5 * dx/(a + V[i]), dt)
                
            # equations 7.54 - 7.56
            row_bar[i] = row[i] + drow[i] * dt
            V_bar[i] = V[i] + dV[i] * dt
            T_bar[i] = T[i] + dT[i] * dt
            
            # equations 7.57 - 7.59
            drow_bar[i] = - row_bar[i] * (V_bar[i] - V_bar[i - 1])/dx - row_bar[i] * V_bar[i] * (math.log(A[i]) - math.log(A[i - 1]))/dx - V_bar[i] * (row_bar[i] - row_bar[i - 1])/dx
            dV_bar[i] = -V_bar[i] * (V_bar[i] - V_bar[i - 1])/dx - 1/lamda *((T_bar[i] - T_bar[i - 1])/dx + T_bar[i]/row_bar[i] * (row_bar[i] - row_bar[i - 1])/dx)
            dT_bar[i] = - V_bar[i] * (T_bar[i] - T_bar[i - 1])/dx - (lamda - 1) * T_bar[i] * ((V_bar[i] - V[i - 1])/dx + V_bar[i] * (math.log(A[i]) - math.log(A[i - 1]))/dx)
            
            # equations 7.60 - 7.62
            drow_ave[i] = .5 * (drow[i] + drow_bar[i])
            dV_ave[i] = .5 * (dV[i] + dV_bar[i])
            dT_ave[i] = .5 * (dT[i] + dT_bar[i])
            
            # equations 7.63 - 7.65
            row[i] = row[i] + drow_ave[i] * dt
            V[i] = V[i] + dV_ave[i] * dt
            T[i] = T[i] + dT_ave[i] * dt
            
            # equations 7.70 - 7.71
            V[0] = 2 * V[1] - V[2]
            row[0] = 1
            T[0] = 1
            
            # equations 7.72a - c
            V[xSteps] = 2 * V[xSteps - 1] - V[xSteps - 2]
            row[xSteps] = 2 * row[xSteps - 1] - row[xSteps - 2]
            T[xSteps] = 2 * T[xSteps -1] - T[xSteps - 2]
            
            mach[i] = V[i]/math.sqrt(T[i])
            
            if i == index_for_graph:
                row_hist[t] = row[i]
                V_hist[t] = V[i]
                T_hist[t] = T[i]
                mach_hist[t] = mach[i]
            
    return row, V, T, row_hist, V_hist, T_hist, mach_hist

def graphs(row, T, V, row_hist, V_hist, T_hist, mach_hist, A, xSteps, dx, timeSteps):
    timeStep_axis = []
    for t in range(timeSteps):
        timeStep_axis.append(t)
    x_axis = []
    for i in range(xSteps + 1):
        x_axis.append(i * dx)
    
    A_negative = []
    for i in range(xSteps + 1):
        A_negative.append(-(1 + 2.2*(i * dx - 1.5)*(i * dx - 1.5)))
    
    print("\n\n After %d timesteps:" % timeSteps)
    print(" %8s  %12s  %12s  %12s  %12s" % ("index", "x", "rho", "V", "T"))
    x = 0
    for i in range(xSteps + 1):
        print(" %8d  %12.6f  %12.6f  %12.6f  %12.6f" % (i, x, row[i], V[i], T[i]))
        x += dx
    
    # graph nozzle geometry
    plt.plot(x_axis, A, color = "blue")
    plt.plot(x_axis, A_negative, color = "blue")
    plt.title("Nozzle Geometry")
    plt.xlabel("x")
    plt.show()
    
    plt.plot(timeStep_axis, row_hist, label = "rho")
    plt.plot(timeStep_axis, V_hist, label = "V")
    plt.plot(timeStep_axis, T_hist, label = "T")
    plt.plot(timeStep_axis, mach_hist, label = "M")
    plt.title("where x = 1.5")
    plt.xlabel("timesteps")
    plt.legend()
    plt.show()

#Main body of the code

#Prompt the user for inputs
#xMin = float(input("xMin = "))
#xMax = float(input("xMax = "))
#xSteps = int(input("xInterval = "))
xSteps = 100
xMin = 0
xMax = 3
dx = (xMax - xMin)/xSteps
timeSteps = 1000
index_for_graph = 50

A, row, V, T = CalculateTable(xMin,xMax,xSteps)
row, V, T, row_hist, V_hist, T_hist, mach_hist= timeStepping(A, T, row, V, timeSteps, xSteps, dx, index_for_graph)
graphs(row, T, V, row_hist, V_hist, T_hist, mach_hist, A, xSteps, dx, timeSteps)
