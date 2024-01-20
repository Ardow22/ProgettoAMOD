
from Utils import fileHandler
from Clark_Wright import Clark_wright
from Sweep_Algorithm import Sweep
from My_Algorithm import My_algorithm
from My_Algorithm_2 import My_algorithm_2
from My_Algorithm_3 import My_algorithm_3

import time




def main(): #main serve ad eseguire il codice su una istanza specifica
    dir1 = './VRP_instances'  #directory dove ci sono tutte le istanza
    filename = "A-n32-k5.txt" #nome del file che si vuole analizzare
    customers = fileHandler.numberOfCustomer(dir1 + "/" + filename) #lettura del numero dei clienti dell'istanza
    real_customers = customers - 1  #il primo elemento è il deposito, quindi viene tolto dal numero reale dei clienti
    print("Il numero dei clienti per questa istanza è " + str(real_customers))
    capacity = fileHandler.valueOfCapacity(dir1 + "/" + filename) #lettura della capacità dei veicolo dell'istanza
    print("La capacità del veicolo per questa istanza è " + str(capacity))
    opt = fileHandler.optimumValue(dir1 + "/" + filename) #lettura del valore ottimo dell'istanza
    print("Il valore ottimo per questa istanza è " + str(opt))

    demandList = fileHandler.demandDictionary(dir1 + "/" + filename, customers) #creazione di un elenco con la domanda di ogni cliente (la lista va dall'indice 0 all'indice n-1, mentre i clienti sono n)
    demandList.remove(str(0)) #rimozione del primo elemento dalla lista perché è il nodo deposito
    print("L'elenco delle domande per questa istanza è " + str(demandList))
    coordList = fileHandler.coordDictionary(dir1 + "/" + filename, customers)  # creazione di un dizionario con le coordinate di ciascun cliente
    list_temp = fileHandler.createDistance(customers, coordList)  #lista temporanea per calcolare le distanze tra i vari clienti con il deposito incluso
    depotDistance = list_temp[0]  #memorizzo le distanze del deposito da tutti gli altri nodi in una lista a parte
    print("L'elenco con le distanze per il deposito è ", depotDistance)
    depo_coord = coordList[0]
    coordList.pop(0)  #rimozione del primo elemento dalla lista perché è il nodo deposito
    print("L'elenco delle coordinate per questa istanza è " + str(coordList))
    print("Le coordinate del deposito sono: ", depo_coord)
    distanceList = fileHandler.createDistance(real_customers, coordList) #lista con le reali distanze tra i clienti senza il deposito
    print("L'elenco con le distanze è ", distanceList)

    print(" CLARKE&WRIGHT ALGORITHM ")
    t1_1 = time.time()
    solution_1 = Clark_wright.algorithm(real_customers, distanceList, capacity, demandList, depotDistance)
    error1 = ((solution_1 - int(opt)) / int(opt)) * 100  # calcolo l'errore percentuale
    print("Errore percentuale: ", error1)
    t2_1= time.time()
    t_1 = t2_1 - t1_1 #calcolo del tempo di esecuzione dell'algoritmo
    print("Il tempo impiegato dall'algoritmo di Clark&Wright in secondi è: ", t_1)
    print("\n")

    print(" SWEEP ALGORITHM ")
    t1_2 = time.time()
    solution_2 = Sweep.algorithm(depo_coord, coordList, capacity, demandList, distanceList, depotDistance)
    error2 = ((solution_2 - int(opt)) / int(opt)) * 100  # calcolo l'errore percentuale
    print("Errore percentuale: ", error2)
    t2_2 = time.time()
    t_2 = t2_2 - t1_2
    print("Il tempo impiegato dall'algoritmo Sweep in secondi è: ", t_2)
    print("\n")

    print(" \n\n\nMY ALGORITHM 1 ")
    t1_3 = time.time()
    solution_3 = My_algorithm.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
    error3 = ((solution_3 - int(opt)) / int(opt)) * 100  # calcolo l'errore percentuale
    print("Errore percentuale: ", error3)
    t2_3 = time.time()
    t_3 = t2_3 - t1_3
    print("Il tempo impiegato dall' algoritmo euristico 1 in secondi è: ", t_3)

    print(" \n\n\nMY ALGORITHM 2 ")
    t1_4 = time.time()
    solution_4 = My_algorithm_2.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
    error4 = ((solution_4 - int(opt)) / int(opt)) * 100  # calcolo l'errore percentuale
    print("Errore percentuale: ", error4)
    t2_4 = time.time()
    t_4 = t2_4 - t1_4
    print("Il tempo impiegato dall' algoritmo euristico 2 in secondi è: ", t_4)

    print(" \n\n\nMY ALGORITHM 3 ")
    t1_5 = time.time()
    solution_5 = My_algorithm_3.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
    error5 = ((solution_5 - int(opt)) / int(opt)) * 100  # calcolo l'errore percentuale
    print("Errore percentuale: ", error5)
    t2_5 = time.time()
    t_5 = t2_5 - t1_5
    print("Il tempo impiegato dall' algoritmo euristico 3 in secondi è: ", t_5)

main()
