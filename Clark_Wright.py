import re

def saving(distanceList, nr1, nr2, depotDistance): #funzione per il calcolo del saving
    distance1 = depotDistance[nr1+1] #dist tra dep e index
    distance2 = depotDistance[nr2+1] #dist tra dep e i
    distance3 = distanceList[nr1][nr2] #dist tra i e index
    result = distance1 + distance2 - distance3
    return result

def which_route(key, routes): #La funzione prende in argomento la coppia che è chiave per i saving e i percorsi trovati fino ad ora
    node_sel = list()
    i_route = [-1, -1]
    count_in = 0
    for route in routes: #scorro su tutti percorsi
        for k in key: #se ho [12, 5] questo ciclo for mi deve far andare prima in 12 e poi in 5
            try:
                route.index(k) #cerco l'indice più basso nell'elenco in cui appare l'elemento cercato k
                i_route[count_in] = routes.index(route)
                node_sel.append(k)
                count_in = count_in + 1
            except:
                pass
    if i_route[0] == i_route[1]:
        overlap = 1
    else:
        overlap = 0

    return node_sel, count_in, i_route, overlap


def sum_cap(route, demandList): #funzione per il calcolo della capacità
    sum_cap = 0
    for r in route:
        demand = int(demandList[int(r)-1])
        sum_cap = sum_cap + demand
    return sum_cap


def interior(node, route):#tale funzione serve a verificare che node sia dentro alla route
    try:
        i = route.index(node)
        if i == 0 or i == (len(route) - 1):
            label = False
        else:
            label = True
    except:
        label = False
    return label


def merge(route0, route1, link): #tale funzione serve ad unire due percorsi
    if route0.index(link[0]) != (len(route0) - 1):
        route0.reverse()

    if route1.index(link[1]) != 0:
        route1.reverse()

    return route0 + route1

def calculate_total_distance(route, d_list, depot_list): #funzione ausiliaria per calcolare la distanza totale di ogni percorso
    total_distance = 0
    for i in range(len(route) - 1):
        if i == 0:
            distance = depot_list[int(route[1])]
        elif i == (len(route) - 2):
            distance = depot_list[int(route[i])]
        else:
            distance = d_list[int(route[i]) - 1][int(route[i + 1]) - 1]
        total_distance = total_distance + distance
    return total_distance

def calculate_solution(route, d_list, depot_dist): #funzione ausiliaria per il calcolo della soluzione
    route.append(0) #inserimento del nodo deposito alla fine del percorso
    route.insert(0, 0) #inserimento del nodo deposito all'inizio del percorso
    solution = calculate_total_distance(route, d_list, depot_dist)
    return solution

class Clark_wright:

    def algorithm(total, distanceList, capacity, demandList, depotDistance): #esecuzione dell'algoritmo di Clark e Wright
        savings = dict()
        index = 0
        while (index < total):
            for i in range(total):
                if i != index:
                    a = max(index, i) + 1#aggiungo +1 perché l'elemento di indice 0 è il cliente 1 e così via
                    b = min(index, i) + 1
                    key = '(' + str(a) + ',' + str(b) + ')'
                    savings[key] = saving(distanceList, index, i, depotDistance)#distanza tra deposito ed index + distanza tra deposito ed i - distanza tra i e index
                if (i == total - 1):
                    index = index + 1

        sorted_saving_by_value = sorted(savings.items(), key=lambda x: x[1], reverse=True)
        decrescent_saving = dict(sorted_saving_by_value) #elenco dei saving messo in ordine decrescente
        print("la savings vale " + str(decrescent_saving))

        routes = list()
        remaining = True
        step = 0
        node_list = list()
        for i in range(total+1):
            if (i > 0):
                node_list.append(i) #riempio la lista con tutti i nodi, tranne il deposito
        for k in decrescent_saving.keys(): #scorro le chiavi del dizionario dei saving
            step = step + 1
            if remaining:
                print("Iterazione ", step, ":")
                new_k = re.findall(r'\d+', k)
                node_sel, num_in, i_route, overlap = which_route(new_k, routes)

                if num_in == 0:
                    if sum_cap(new_k, demandList) <= capacity:
                        routes.append(new_k)
                        node_list.remove(int(new_k[0]))
                        node_list.remove(int(new_k[1]))
                        print('\t', 'La coppia ', new_k, ' soddisfa i criteri a), per questo è inserito come nuovo percorso')
                    else:
                        print('\t', 'Nonostante la coppia ', new_k,
                              ' soddisfi i criteri a), eccede la capacità massima, quindi tale coppia viene saltata')

                elif num_in == 1:
                    n_sel = node_sel[0]
                    i_rt = i_route[0]
                    position = routes[i_rt].index(n_sel)
                    k_temp = new_k
                    k_temp.remove(n_sel)
                    node = k_temp[0]

                    cond1 = (not interior(n_sel, routes[i_rt]))
                    cond2 = (sum_cap(routes[i_rt] + [node], demandList) <= capacity)

                    if cond1:
                        if cond2:
                            print('\t', 'la coppia ', new_k, ' soddisfa i criteri b), un nuovo nodo è aggiunto al percorso ',
                                  routes[i_rt], '.')
                            if position == 0:
                                routes[i_rt].insert(0, node)
                            else:
                                routes[i_rt].append(node)
                            node_list.remove(int(node))

                        else:
                            print('\t', 'Sebbene la coppia ', new_k,
                                  ' soddisfi i criteri b), esso eccede la capacità massima, quindi tale coppia viene saltata')
                            continue
                    else:
                        print('\t', 'Per la coppia ', new_k, ', il nodo ', n_sel, ' è interno al percorso ', routes[i_rt],
                              ', quindi viene saltata')
                        continue

                else:
                    if overlap == 0:
                        cond1 = (not interior(node_sel[0], routes[i_route[0]]))
                        cond2 = (not interior(node_sel[1], routes[i_route[1]]))
                        cond3 = (sum_cap(routes[i_route[0]] + routes[i_route[1]], demandList) <= capacity)

                        if cond1 and cond2:
                            if cond3:
                                route_temp = merge(routes[i_route[0]], routes[i_route[1]], node_sel)
                                temp1 = routes[i_route[0]]
                                temp2 = routes[i_route[1]]
                                routes.remove(temp1)
                                routes.remove(temp2)
                                routes.append(route_temp)
                                try:
                                    node_list.remove(new_k[0])
                                    node_list.remove(new_k[1])
                                except:
                                    pass
                                print('\t', 'la coppia ', new_k, ' soddisfa i criteri c), così il percorso ', temp1, ' ed il percorso ',
                                      temp2, ' vengono uniti')
                            else:
                                print('\t', 'Nonostante la coppia ', new_k,
                                      ' soddisfi i criteri c), essa eccede la capacità massima, quindi tale coppia viene saltata.')
                                continue
                        else:
                            print('\t', 'per la coppia ', new_k,
                                  ', i due nodi si trovano in due differenti percorsi, ma non tutti i nodi soddisfano le richieste interne, così tale coppia viene saltata')
                            continue
                    else:
                        print('\t', 'la coppia ', new_k, ' è già inclusa nei percorsi')
                        continue

                for route in routes:
                    print('\t', 'percorso: ', route, ' con carico ', sum_cap(route, demandList))
            else:
                print('-------')
                print("Tutti i nodi sono inclusi nei percorsi, l'algoritmo termina")
                break

            remaining = bool(len(node_list) > 0)

        for node_o in node_list:
            routes.append([node_o])

        print('------')
        print('I percorsi trovati sono: ')
        print(routes)

        solution = 0
        for i in range(len(routes)):
            solution = solution + calculate_solution(routes[i], distanceList, depotDistance)
        print("Soluzione: ", solution)


        return solution









