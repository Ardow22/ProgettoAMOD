import re
import math
import csv
import os



class fileHandler:
    def numberOfCustomer(path):#funzione per estrapolare il numero di clienti
        file = open(path, "r")
        count = 0
        while count < 4: #nel formato dei file l'informazioni sul numero dei clienti si trova alla quarta riga
           riga = file.readline()
           count = count + 1
           if count == 4:
               file.close()
               return int(re.search(r'\d+', riga).group())
        return 0

    def valueOfCapacity(path):#funzione per estrapolare la capacità del veicolo
        file = open(path, "r")
        count = 0
        while count < 6: #nel formato dei file l'informazioni sulla capacità del veicolo si trova alla sesta riga
           riga = file.readline()
           count = count + 1
           if count == 6:
               file.close()
               return int(re.search(r'\d+', riga).group())
        return 0

    def optimumValue(path):#funzione per estrapolare il valore ottimo
        file = open(path, "r")
        count = 0
        while count < 2: #nel formato dei file l'informazioni sul valore ottimo del problema si trova alla seconda riga
           riga = file.readline()
           count = count + 1
           if count == 2:
               numbers = re.findall(r'\d+', riga)
               file.close()
               return numbers[1]
        return 0

    def coordDictionary(path, total):
        coordList = list() #elenco che verrà riempito con tutti i dizionari contenenti le coordinate di ogni cliente
        file = open(path, "r")
        count = 0
        while count < 7:
            riga = file.readline()
            count = count + 1

        count = 0
        while count < total:
            riga = file.readline()
            count = count + 1
            numbers = re.findall(r'\d+', riga)
            coordDict = {"x": numbers[1], "y": numbers[2]} #creazione di un dizionario con le coordinate x ed y del cliente
            coordList.append(coordDict)
        file.close()
        return coordList

    def demandDictionary(path, total):
        demandList = list()
        file = open(path, "r")
        count = 0
        while count < 8+total:
            riga = file.readline()
            count = count + 1

        count = 0
        while count < total:
            riga = file.readline()
            count = count + 1
            numbers = re.findall(r'\d+', riga)
            demandList.append(numbers[1])
        return demandList

    def createDistance(total, xyList): #funzione per calcolare la distanze tra i vari clienti partendo dalle posizioni in coordinate x e y
        index = 0
        distanceList = list()
        while index < total:
            distanceSingleClient = list()
            for i in range(len(xyList)):
                p1 = list()
                p2 = list()
                p1.append(int(xyList[index]["x"]))
                p1.append(int(xyList[index]["y"]))
                p2.append(int(xyList[i]["x"]))
                p2.append(int(xyList[i]["y"]))
                result = math.dist(p1, p2) #calcolo della distanza tra due punti
                result2 = round(result) #arrotondamento per difetto della distanza
                distanceSingleClient.append(result2)
            index = index + 1
            distanceList.append(distanceSingleClient)

        return distanceList

    def createCSV(results_list): #funzione che crea il CSV finale con i dati ottenute da tutte le istanze
        dir = './VRP_instances'
        fileCSV = 'results.csv'
        #with open(dir + "/" + fileCSV, 'w') as csvfile:
        with open(fileCSV, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Nome file", "Numero clienti", "Capacità veicolo", "Soluzione ottima", "Soluzione Clark&Wright", "Errore Clark&Wright", "Tempo di esecuzione Clark&Wright", "Soluzione Sweep", "Errore Sweep", "Tempo di esecuzione Sweep", "Soluzione MyAlgorithm1", "Errore MyAlgorithm1", "Tempo di esecuzione MyAlgorithm1", "Soluzione MyAlgorithm2", "Errore MyAlgorithm2", "Tempo di esecuzione MyAlgorithm2", "Soluzione MyAlgorithm3", "Errore MyAlgorithm3", "Tempo di esecuzione MyAlgorithm3"])
            for i in range(len(results_list)):
                writer.writerow(results_list[i])
                writer.writerow(";")




