from Utils import fileHandler
from Clark_Wright import Clark_wright
from Sweep_Algorithm import Sweep
from My_Algorithm import My_algorithm
from My_Algorithm_2 import My_algorithm_2
from My_Algorithm_3 import My_algorithm_3
import time
from os import listdir
from os.path import isfile, join


def main2(): #main2 serve ad eseguire il codice su tutte le istanze
    dir1 = './VRP_instances' #directory dove ci sono tutte le istanze
    onlyfiles = [
        f for f in listdir(dir1)
        if isfile(join(dir1, f))
           and f.endswith(('.txt'))
    ]

    total_results = list() #lista contenente tutte le liste con i dati delle istanze da inserire poi in tabella

    for nameFile in onlyfiles:
        single_result = list() #lista in cui verranno inseriti tutti i dati utili ad analizzare l'istanza
        filename = nameFile  # nome del file che si vuole analizzare
        single_result.append(filename)
        customers = fileHandler.numberOfCustomer(dir1 + "/" + filename)  # lettura del numero dei clienti dell'istanza
        real_customers = customers - 1  # il primo elemento è il deposito
        print("Il numero dei clienti per questa istanza è " + str(real_customers))
        single_result.append(real_customers)
        capacity = fileHandler.valueOfCapacity(dir1 + "/" + filename)  # lettura della capacità dei veicolo dell'istanza
        print("La capacità del veicolo per questa istanza è " + str(capacity))
        single_result.append(capacity)
        opt = fileHandler.optimumValue(dir1 + "/" + filename)  # lettura del valore ottimo dell'istanza
        print("Il valore ottimo per questa istanza è " + str(opt))
        single_result.append(opt)

        demandList = fileHandler.demandDictionary(dir1 + "/" + filename, customers)  # creazione di un elenco con la domanda di ogni cliente (la lista va dall'indice 0 all'indice n-1, mentre i clienti sono n)
        demandList.remove(str(0))  # rimozione del primo elemento dalla lista perché è il nodo deposito
        print("L'elenco delle domande per questa istanza è " + str(demandList))
        coordList = fileHandler.coordDictionary(dir1 + "/" + filename, customers)  # creazione di un dizionario con le coordinate di ciascun cliente
        list_temp = fileHandler.createDistance(customers, coordList)  # lista temporanea per calcolare le distanze tra i vari clienti con il deposito incluso
        depotDistance = list_temp[0]  # memorizzo le distanze del deposito da tutti gli altri nodi in una lista a parte
        print("L'elenco con le distanze per il deposito è ", depotDistance)
        depo_coord = coordList[0]
        coordList.pop(0)  # rimozione del primo elemento dalla lista perché è il nodo deposito
        print("L'elenco delle coordinate per questa istanza è " + str(coordList))
        print("Le coordinate del deposito sono: ", depo_coord)
        distanceList = fileHandler.createDistance(real_customers, coordList)  # lista con le reali distanze tra i clienti senza il deposito
        print("L'elenco con le distanze è ", distanceList)

        print("\n\n\n CLARKE&WRIGHT ALGORITHM ")
        t1_1 = time.time()
        solution_1 = Clark_wright.algorithm(real_customers, distanceList, capacity, demandList, depotDistance)
        error1 = ((solution_1 - int(opt))/int(opt))*100 #calcolo l'errore percentuale
        print("Errore percentuale: ", error1)
        single_result.append(solution_1)
        single_result.append(error1)
        t2_1 = time.time()
        t_1 = t2_1 - t1_1 #calcolo del tempo di esecuzione
        single_result.append(t_1)
        print("Il tempo impiegato dall'algoritmo di Clark&Wright in secondi è: ", t_1)

        print("\n\n\n SWEEP ALGORITHM ")
        t1_2 = time.time()
        solution_2 = Sweep.algorithm(depo_coord, coordList, capacity, demandList, distanceList, depotDistance)
        error2 = ((solution_2 - int(opt))/int(opt))*100
        print("Errore percentuale: ", error2)
        single_result.append(solution_2)
        single_result.append(error2)
        t2_2 = time.time()
        t_2 = t2_2 - t1_2
        single_result.append(t_2)
        print("Il tempo impiegato dall'algoritmo Sweep in secondi è: ", t_2)

        print("\n\n\n MY ALGORITHM 1")
        t1_3 = time.time()
        solution_3 = My_algorithm.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
        error3 = ((solution_3 - int(opt))/int(opt))*100
        print("Errore percentuale: ", error3)
        single_result.append(solution_3)
        single_result.append(error3)
        t2_3 = time.time()
        t_3 = t2_3 - t1_3
        single_result.append(t_3)
        print("Il tempo impiegato dall'algoritmo euristico 1 in secondi è: ", t_3)

        print(" \n\n\n MY ALGORITHM 2 ")
        t1_4 = time.time()
        solution_4 = My_algorithm_2.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
        error4 = ((solution_4 - int(opt))/int(opt))*100
        print("Errore percentuale: ", error4)
        single_result.append(solution_4)
        single_result.append(error4)
        t2_4 = time.time()
        t_4 = t2_4 - t1_4
        single_result.append(t_4)
        print("Il tempo impiegato dall' algoritmo euristico 2 in secondi è: ", t_4)

        print(" \n\n\n MY ALGORITHM 3 ")
        t1_5 = time.time()
        solution_5 = My_algorithm_3.algorithm(depotDistance, distanceList, capacity, demandList, real_customers)
        error5 = ((solution_5 - int(opt))/int(opt))*100
        print("Errore percentuale: ", error5)
        single_result.append(solution_5)
        single_result.append(error5)
        t2_5 = time.time()
        t_5 = t2_5 - t1_5
        single_result.append(t_5)
        print("Il tempo impiegato dall' algoritmo euristico 3 in secondi è: ", t_5)

        total_results.append(single_result)

    fileHandler.createCSV(total_results)


main2()
