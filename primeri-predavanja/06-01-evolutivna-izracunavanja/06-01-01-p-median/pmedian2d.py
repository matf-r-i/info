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

# fitnes je ovde isti kao i funkcija cilja, a to je suma udaljenosti svih kupaca do svojih najblizih prodavnica
def fitness(problem, solvect):
    fit = 0
    for (x,y) in problem:
        mindist = float("Inf")
        mini = -1
        for i in range(len(solvect)):
            (p,q) = solvect[i]
            d = dist((x,y),(p,q))
            if d<mindist:
                mindist = d
                mini = i
        fit+=mindist
    return fit

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def randomPoint():
    return (random.randrange(100),random.randrange(100))

# jedno resenje je vektor velicine p gde je svaka koordinata vektora uredjeni par - 2D koordinata
def randomSolution(problem, p):
    solvect = [randomPoint() for i in range(p)]
    fit = fitness(problem,solvect)
    return (solvect,fit)

# slucajna pretraga
def randomSearch(problem, p):
    itmax = 50000
    bestsol = randomSolution(problem,p)
    # itmax puta generisemo novo slucajno resenje i pamtimo najbolje
    for it in range(itmax):
        newsol = randomSolution(problem, p)
        if newsol[1]<bestsol[1]:
            bestsol = newsol
            print('Poboljsanje '+str(it)+' '+str(bestsol[1]))
        #if it%500==0:
        #    showProblemAndSolution(problem,bestsol)
    showProblemAndSolution(problem,bestsol)

# nasumicna inicijalizacija je najpogodnija, jer ne zanemaruje statisticki nijedan deo prostora pretrage
def initPop(problem, p, n):
    pop = [randomSolution(problem,p) for i in range(n)]
    return pop

def selectRandom(pop):
    return pop[random.randrange(len(pop))]

# turnirska selekcija je uopstenje slucajne kada je velicina turnira 1
# kada je velicina turnira cela populacija, onda se selekcija svodi na elitisticku
def selectTournament(pop, ts):
    tpop = [pop[random.randrange(len(pop))] for i in range(ts)]
    # :)
    tpop = order(tpop)
    return tpop[0]

# jednopoziciono ukrstanje - 2 deteta od 2 roditelja xxxxxx,  yyyyyy -> xxyyyy, yyxxxx 
def crossOver(problem, p1, p2):
    # slucajno biramo poziciju oko koje ukrstamo
    pos = random.randrange(len(p1[0]))
    c1vect = p1[0][:pos]+p2[0][pos:]
    c2vect = p2[0][:pos]+p1[0][pos:]
    return (c1vect,fitness(problem, c1vect)), (c2vect,fitness(problem,c2vect))

# sortiranje populacije
def order(pop):
    pop = sorted(pop,key=lambda x:x[1])
    return pop

# po svakoj 2D koordinati je verovatnoca mutacije mutprob
def mutate(problem, sol, mutprob):
    for i in range(len(sol[0])):
        if random.random()<mutprob:
            # mutiranje u ovom slucaju je prosto dodeljivanje slucajne 2D koordinate
            sol[0][i]=randomPoint()
    return (sol[0], fitness(problem, sol[0]))

# uopsteni evolutivni algoritam (ovo najvise lici na genetski, ali nije bas potpuno isto)
def ea(problem, p):
    # velicina populacije
    popsize = 20 
    # broj iteracija - kako bi resenja bila uporediva sa radom slucajne pretrage, trudimo se
    # da ukupan broj izvrsavanja fitnes funkcije bude isti (50000 = 20 x 2500)
    maxit = 2500
    # verovatnoca mutacije
    mutprob = 0.1
    pop = initPop(problem, p, popsize)
    for it in range(maxit):
        pop = order(pop)
        if it % 100 == 0:
            print('Iteracija '+str(it)+' '+str(pop[0][1]))
        # formiramo novu populaciju, u koju direktno prebacujemo 2 najbolja resenja
        # ovo je elitizam i praktican nam je, jer na taj nacin nemamo oscilacije u radu algoritma
        # tj. najbolje resenje se nikad ne povecava, vec se samo smanjuje. 
        # ne sme se preterivati sa elitizmom, jer se njime drasticno povecava selekcioni pritisak. 
        newpop = [pop[0],pop[1]]
        for i in range(len(pop)//2-1):
            # preostalih popsize-2 clanova populacije dobijamo tako sto popsize/2-1 puta biramo po dva roditelja
            # i potom ih ukrstamo. 
            # testirati sa razlicitim operatorima selekcije i analizirati selekcioni pritisak. 
            # implementirati i fitnes-srazmernu selekciju putem ruletskog tocka. 
            p1 = selectTournament(pop, 2)
            p2 = selectTournament(pop,2)
            c1, c2 = crossOver(problem,p1,p2)
            c1 = mutate(problem, c1, mutprob)
            c2 = mutate(problem, c2, mutprob)
            newpop.append(c1)
            newpop.append(c2)
        pop = newpop
    showProblemAndSolution(problem,pop[0])
    
# pokretanje algoritma, ali pre toga podesavamo generator pseudoslucajnih brojeva da bismo 
# u razlicitim pokretanjim sa npr. razlicitim parametrima algoritma imali konzistentne (uporedive) rezultate. 
random.seed(11111)
#randomSearch(problem1,p)
ea(problem1,p)


