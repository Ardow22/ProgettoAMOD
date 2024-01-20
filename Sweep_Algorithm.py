from math import degrees, atan2
import random

def angle_calculate(x, y): #funzione ausiliaria per calcolare l'angolo di ogni nodo
    angle = degrees(atan2(y, x))
    return angle

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

def calculate_total_distance2_opt(route, d_list): #funzione ausiliaria per calcolare la distanza totale di ogni percorso
    total_distance = 0
    for i in range(len(route) - 1):
        distance = d_list[int(route[i]) - 1][int(route[i + 1]) - 1]
        total_distance = total_distance + distance
    return total_distance
def calculate_solution(route, d_list, depot_dist): #funzione ausiliaria per il calcolo della soluzione
    route.append(0) #inserimento del nodo deposito alla fine del percorso
    route.insert(0, 0) #inserimento del nodo deposito all'inizio del percorso
    solution = calculate_total_distance(route, d_list, depot_dist)
    return solution


def two_opt(route, d_list): #funzione per l'esecuzione dell'algoritmo 2-opt su un percorso dato
    best_route = route
    best_distance = calculate_total_distance2_opt(route, d_list)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                new_distance = calculate_total_distance2_opt(new_route, d_list)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True

    return best_route


class Sweep:
    #per prima cosa bisogna traslare tutto il sistema di riferimento. Se, ad esempio, abbiamo il deposito che sta nelle
    #coordinate x = 82, y = 76, allora il vettore di traslazione è (-82, -76), perché x' = x + vx e y' = y + vy.
    #A questo punto vanno traslati tutti i punti dello stesso vettore (-82, -76).
    #Fatto ciò si applica l'algoritmo Sweep

    def algorithm(depo_coord, coord_List, capacity_v, demand_list, dist_list, depot_list):
        vect_traslation = {"x": - int(depo_coord["x"]), "y": - int(depo_coord["y"])} #calcolo del vettore di traslazione per traslare tutte le coordinate dei clienti
        print("Il vettore di traslazione vale ", vect_traslation)
        trasl_coordList = coord_List
        ind = 0
        while ind < len(trasl_coordList): #nel ciclo while avviene il calcolo delle nuove coordinate cartesiane traslate
            trasl_coordList[ind]["x"] = int(trasl_coordList[ind]["x"]) + vect_traslation["x"]
            trasl_coordList[ind]["y"] = int(trasl_coordList[ind]["y"]) + vect_traslation["y"]
            ind = ind + 1
        print("L'elenco delle nuove coordinate per questa istanza è ", trasl_coordList)

        polar_list = dict()
        for i in range(len(trasl_coordList)): #in questo ciclo avviene il calcolo dell'angolo per le coordinate polari
            polar_list[i] = angle_calculate(trasl_coordList[i]["x"], trasl_coordList[i]["y"])

        sorted_polar_by_value = sorted(polar_list.items(), key=lambda x: x[1], reverse=False)
        decrescent_angles = dict(sorted_polar_by_value)
        print("Elenco dei nodi dall'angolo più piccolo all'angolo più grande [MEMO: vanno da 0 ad n-1]: ", decrescent_angles)

        total_cap = 0
        single_cluster = list()
        total_cluster = list()

        for k in decrescent_angles.keys():
            if total_cap + int(demand_list[k]) > capacity_v:
                if int(demand_list[k]) > capacity_v:
                    print("nodo ", k, "non servibile")
                else:
                    total_cluster.append(single_cluster)
                    single_cluster = list()
                    single_cluster.append(k+1)
                    total_cap = 0
            else:
                single_cluster.append(k+1) #k+1 perché bisogna sempre tener conto che le liste vanno da 0 ad n-1
                total_cap = total_cap + int(demand_list[k])
        total_cluster.append(single_cluster)

        route_solution = list()
        for i in range(len(total_cluster)):
            initial_route = random.sample(total_cluster[i], len(total_cluster[i])) #qui avviene il calcolo di una prima soluzione random, da cui partirà poi l'algoritmo 2-opt
            optimized_route = two_opt(initial_route, dist_list)
            route_solution.append(optimized_route)

        print("Percorsi trovati (senza considerare il deposito): ", route_solution)

        solution = 0
        for i in range(len(route_solution)):
            solution = solution + calculate_solution(route_solution[i], dist_list, depot_list)
        print("Soluzione: ", solution)

        return solution




