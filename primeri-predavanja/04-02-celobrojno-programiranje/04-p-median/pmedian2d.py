import matplotlib.pyplot as plt
import math
import random

# p-median problem u ravni koji razmatramo je specijalan slucaj problema opisanog na http://www.math.nsc.ru/AP/benchmarks/P-median/p-med_eng.html
# razlika u odnosu na pomenuti problem je to sto ovde matricu troskova izmedju klijenata (kupaca) i lokacija (prodavnica) racunamo
# putem euklidskih rastojanja u 2D i to sto lokacije mozemo da postavimo na bilo koju lokaciju (sto nije slucaj u p-median problemu).
# ovo pojednostavljenje (koliko znam) cini da problem zapravo ne bude NP-tezak, ali nam je zbog jednostavne vizuelizaciji i postavke 
# praktican da nad njim demonstriramo rad evolutivnog algoritma i algoritma slucajne pretrage. 

# lokacije klijenata na mapi [0,100] x [0,100]
problem1 = [(45,23),(4,2), (51,13), (58,3),(85,5),(15,96), (25,21),(85,12), (5,32),(4,23),(90,83),(79,53),(12,13),(45,3)]
# broj prodavnica koje treba postaviti
p=5
# primer jednog resenja
r1 = [(23,12),(56,3),(10,18),(4,89),(21,10)]

# graficka reprezentacija resenja u ravni
def showProblemAndSolution(prob, sol):
    solvect = sol[0]
    fit = sol[1]
    plt.title('Fitnes: '+str(fit))
    plt.scatter([x for (x,y) in prob], [y for (x,y) in prob], c='b')
    plt.scatter([x for (x,y) in solvect], [y for (x,y) in solvect], c='r')
    plt.show()

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))


