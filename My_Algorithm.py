import copy

def calculate_total_distance(route, d_list, depot_list): #funzione ausiliaria per calcolare la distanza totale di ogni percorso
    total_distance = 0
    for i in range(len(route) - 1):
        if i == 0:
            distance = depot_list[route[1]]
        elif i == (len(route) - 2):
            distance = depot_list[route[i]]
        else:
            distance = d_list[int(route[i]) - 1][int(route[i + 1]) - 1]
        total_distance = total_distance + distance
    return total_distance

def calculate_solution(route, d_list, depot_dist): #funzione ausiliaria per il calcolo della soluzione
    route.append(0) #inserimento del nodo deposito alla fine del percorso
    route.insert(0, 0) #inserimento del nodo deposito all'inizio del percorso
    solution = calculate_total_distance(route, d_list, depot_dist)
    return solution
class My_algorithm:

    def algorithm(depot_distance, distance_list, capacity_v, demand_List, total):#in argomento abbiamo la distanza di tutti i nodi dal deposito, la lista di liste con le distanza di ogni nodo da ogni altro nodo e la capacità del veicolo
       depot_copy = copy.deepcopy(depot_distance)#qui avviene la copia l'elenco con le distanze dei nodi dal deposito in modo da poterlo modificare
       depot_dict = dict()#creazione del dizionario con le distanze dal deposito in modo da poter eliminare i nodi scelti con più facilità
       for i in range(len(depot_copy)):
           depot_dict[i] = depot_copy[i]
       depot_dict.pop(0) #eliminazione di 0, in quanto è la distanza del deposito dal deposito
       sorted_depot_by_value = sorted(depot_dict.items(), key=lambda x: x[1], reverse=False)
       crescent_depot = dict(sorted_depot_by_value) #ordinamento in ordine crescente delle distanze dal deposito

       distance_copy = copy.deepcopy(distance_list) #copiamo la lista con le distanze di tutti i nodi con tutti i nodi


       total_customer = list() #questa lista conterrà tutti i diversi percorsi trovati
       nodes_visitated = list() #lista che tiene conto dei nodi visitati
       count = 0 #contatore ausiliario
       error = 0
       while (len(nodes_visitated) < total): #primo ciclo va avanti fino a quando il dizionario delle distanze dal deposito non è nullo
           error = 1
           print("Sono nel deposito ed il numero di nodi rimanenti da visitare è: ", len(crescent_depot))
           print("I nodi visitabili da tale nodo sono (nodo: distanza): ", crescent_depot)
           print("domande: ", demand_List)
           customer = list() #creo la lista che conterrà i clienti possibili fino al limite della capacità del veicolo
           total_capacity = 0
           for key in crescent_depot:  #ciclo per prendere il primo elemento dal dizionario delle distanze dal deposito
               min_node = key
               if int(demand_List[min_node - 1]) <= capacity_v: #vado a prendere il nodo più vicino che ha domanda compatibile con la capacità del veicolo
                   total_capacity = total_capacity + int(demand_List[min_node - 1]) #aggiornamento domanda totale
                   error = 0
                   break
           if (error == 1):
               print("Non ci sono nodi da visitare")
               break
           print("Viene aggiunto ai nodi da visitare il nodo ", min_node)
           print("Aggiornamento domanda totale: ", total_capacity)
           customer.append(min_node) #aggiungo alla lista dei clienti da servire il nodo a distanza minima
           crescent_depot.pop(min_node) #elimino dal dizionario l'elemento appena inserito nella lista dei clienti da servire
           nodes_visitated.append(min_node) #aggiorno l'elenco con i nodi visitati

           while total_capacity <= capacity_v: #questo secondo ciclo while va avanti fino a quando non ho raggiunto la capcità massima del veicolo
               error = 1
               control = 0
               distance_dict = dict()
               print("Sono nel nodo ", min_node)
               for i in range(len(distance_copy[min_node - 1])):
                   distance_dict[i+1] = distance_copy[min_node-1][i]

               for temp_key in distance_dict:
                   if distance_dict[temp_key] == 0:
                       break
               distance_dict.pop(temp_key) #eliminazione del nodo in cui la distanza è 0, perché significa che è il nodo stesso

               if count >= 1:
                   delete_list = list()
                   for temp_key in distance_dict:
                       if temp_key in nodes_visitated:
                           delete_list.append(temp_key)

                   for i in delete_list:
                       distance_dict.pop(i) #eliminazione di tutti i nodi già visitati dalla lista delle distanze

               sorted_distance_by_value = sorted(distance_dict.items(), key=lambda x: x[1], reverse=False)
               crescent_distance = dict(sorted_distance_by_value)
               print("I nodi visitabili da tale nodo sono (nodo: distanza): ", crescent_distance)
               print("domande: ", demand_List)
               if len(crescent_distance) == 0: #se non ci sono nodi da visitare esco dal ciclo
                   break
               for k in crescent_distance:
                   min_node = k
                   if int(demand_List[min_node - 1]) <= capacity_v:
                       error = 0
                       temp_capacity = total_capacity + int(demand_List[min_node - 1])
                       if temp_capacity <= capacity_v:
                           control = 1
                           break
               if error == 1 or control == 0: #controllo se aggiungendo il nuovo nodo viene superata la capacità del veicolo
                   delete_list_depot = list()
                   for temp_key in crescent_depot:
                       if temp_key in nodes_visitated:
                           delete_list_depot.append(temp_key)
                   for i in delete_list_depot:
                       crescent_depot.pop(i)
                   break
               else:
                   print("Aggiungo il nodo ", min_node)
                   total_capacity = temp_capacity #aggiornamento della domanda totale
                   print("Aggiornamento domanda totale: ", total_capacity)
                   customer.append(min_node) #aggiungo il nodo al percorso di clienti attuale
                   crescent_distance.pop(min_node)
               if min_node in nodes_visitated:
                   break
               else:
                   nodes_visitated.append(min_node) #aggiungo il nodo alla lista di nodi già visitati
               count = count + 1

           total_customer.append(customer)

       print("I percorsi trovati sono: ", total_customer)
       solution = 0
       for i in range(len(total_customer)):
           solution = solution + calculate_solution(total_customer[i], distance_list, depot_distance)
       print("Soluzione: ", solution)

       return solution






