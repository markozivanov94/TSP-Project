import matplotlib.pyplot as plt
import numpy as np

import math
import random
from time import time


class TSP:
    def __init__(self, n=100):
        self.cities = self.generate_cities(n)
        self.cost_mat = self.make_cost_mat()

    # Vraca listu x i y kordinata iz tacaka
    def XY(self, points):
        return [p[0] for p in points], [p[1] for p in points]

    # Plotuje rutu
    def plot_tour(self, tour, cena, algoritam, vreme):
        print(algoritam, cena)
        plt.title("Duzina: " + str(round(cena,3)) + " Algoritam: " + algoritam + " Vreme: " + str(round(vreme, 3)));
        X, Y = self.XY(tour + [tour[0]])
        plt.plot(X, Y, "bo-", alpha=1, markersize=8)
        plt.show()

    # Funkcija za generisanje gradova
    def generate_cities(self, n):
        return list((random.randrange(10, 1200), random.randrange(10, 800)) for c in range(n))

    # Funkcija za racunanje udaljenosti izmedju dva grada
    def distance(self, A, B):
        return math.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))

    # Kreira turu od tacaka
    def create_tour(self, points):
        return [list(self.cities)[i] for i in points]

    # Racuna totalnu distancu izmedju gradova sa zadatom rutom
    def total_distance(self, tour):
        tour = self.create_tour(tour)
        return sum(self.distance(tour[i], tour[i - 1]) for i in range(len(tour)))

    # Racuna da li je veca promena ako se linije zamene
    def cost_change(self, n1, n2, n3, n4):
        return self.cost_mat[n1][n3] + self.cost_mat[n2][n4] - self.cost_mat[n1][n2] - self.cost_mat[n3][n4]

    # Pravi matricu cena
    def make_cost_mat(self):
        cost_mat = []
        for i in range(len(self.cities)):
            mat = []
            cost_mat.append(mat)
            for j in range(len(self.cities)):
                mat.append(self.distance(self.cities[i], self.cities[j]))
        return cost_mat

    # Brut force algoritam
    def brute_force(self):
        t = time()
        perm = 0
        cities_num = list(range(len(self.cities)))
        best = self.total_distance(cities_num)
        best_route = cities_num
        for p in self.perm_generator(cities_num):
            current = self.total_distance(p)
            if current < best:
                best = current
                best_route = p
            perm += 1
        tsp.plot_tour(self.create_tour(best_route), best, "Brute force", time()-t)

    # Generise sve permutacije iz liste
    def perm_generator(self, lst):
        if len(lst) == 1:
            yield lst
        else:
            for i in range(len(lst)):
                for perm in self.perm_generator(lst[:i] + lst[i + 1:]):
                    yield [lst[i]] + perm

    # Nearest neighbour algoritam
    def nearest_neighbour(self, plot=True):
        t = time()
        route = []
        size = len(self.cities)
        curent_city = np.random.randint(1, size)
        current_best = self.cost_mat[curent_city][0]
        current = curent_city
        for i in range(size):
            for j in range(size):
                if j not in route and curent_city != j:
                    if not current_best:
                        current = j
                        current_best = self.cost_mat[curent_city][j]
                    if self.cost_mat[curent_city][j] < current_best:
                        current = j
                        current_best = self.cost_mat[curent_city][j]
            curent_city = current
            current_best = None
            route.append(current)
        route.append(route[0])
        best = self.total_distance(route)
        route = self.create_tour(route)
        if plot:
            tsp.plot_tour(route, best, "Nearest neighbour", time()-t)
        else:
            return route, best

    # Two opt algortam
    def two_opt(self, plot=True):
        t = time()
        route = list(range(len(self.cities)))
        random.shuffle(route)
        improved = True
        size = len(route)
        while improved:
            improved = False
            for i in range(1, size - 2):
                for j in range(i + 2, size):
                    if self.cost_change(route[i - 1], route[i], route[j - 1], route[j]) < 0:
                        route[i:j] = route[j - 1:i - 1:-1]
                        improved = True
        tour = self.create_tour(route)
        value = self.total_distance(route)
        if plot:
            tsp.plot_tour(tour, value, "2-opt", time()-t)
        else:
            return tour, value

    # Poziva prosledjeni algoritam sve dok se ne desi N iteracija bez promene
    def multiple_calls(self, alg, alg_name, N):
        t = time()
        list_of_cities = list(range(len(self.cities)))
        best_route_multiple = list_of_cities.copy()
        best = None

        without_change = 0
        looped = 0
        while without_change < N:
            looped += 1
            without_change += 1
            current, value = alg(False)
            if not best or value < best:
                without_change = 0
                best_route_multiple = current
                best = value
        tsp.plot_tour(best_route_multiple, best, "Vise " + alg_name + " - " + str(N), time()-t)


tsp = TSP(100)
tsp.nearest_neighbour()
tsp.multiple_calls(tsp.nearest_neighbour, 'nearest neighbour', 50)
if len(tsp.cities) < 10:
    tsp.brute_force()
tsp.two_opt()
tsp.multiple_calls(tsp.two_opt, '2-opt', 50)
