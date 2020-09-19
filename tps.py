import matplotlib.pyplot as plt
import numpy as np

import math
import random


class TSP:
    def __init__(self, n=100):
        self.cities = self.generate_cities(n)
        self.cost_mat = self.make_cost_mat()

    # Vraca listu x i y kordinata iz tacaka
    def XY(self, points):
        return [p[0] for p in points], [p[1] for p in points]

    # Plotuje rutu
    def plot_tour(self, tour, title=None):
        if title:
            plt.title("Ukupna cena je: " + str(title));
        X, Y = self.XY(tour + [tour[0]])
        plt.plot(X, Y, 'bo-', alpha=1, markersize=8)
        plt.show()

    # Funkcija za generisanje gradova
    def generate_cities(self, n):
        return list((random.randrange(10, 800), random.randrange(10, 1200)) for c in range(n))

    # Funkcija za racunanje udaljenosti izmedju dva grada
    def distance(self, A, B):
        return math.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))

    # Kreira turu
    def create_tour(self, route):
        return [list(self.cities)[i] for i in route]

    # Racuna totalnu udaljenost izmedju gradova sa zadatom rutom
    def total_distance(self, tour):
        tour = self.create_tour(tour)
        return sum(self.distance(tour[i], tour[i - 1]) for i in range(len(tour)))

    def cost_change(self, n1, n2, n3, n4):
        return self.cost_mat[n1][n3] + self.cost_mat[n2][n4] - self.cost_mat[n1][n2] - self.cost_mat[n3][n4]

    def make_cost_mat(self):
        cost_mat = []
        for i in range(len(self.cities)):
            mat = []
            cost_mat.append(mat)
            for j in range(len(self.cities)):
                mat.append(self.distance(self.cities[i], self.cities[j]))
        return cost_mat

    def two_opt(self, route):
        improved = True
        size = len(route)
        while improved:
            improved = False
            for i in range(1, size - 2):
                for j in range(i + 2, size):
                    if self.cost_change(route[i - 1], route[i], route[j - 1], route[j]) < 0:
                        route[i:j] = route[j - 1:i - 1:-1]
                        improved = True
        return route

    def multiple_two_opt(self, out_len):
        list_of_cities = list(range(len(self.cities)))
        best_route_multiple = list_of_cities.copy()

        best = self.total_distance(best_route_multiple)

        without_change = 0
        looped = 0
        while without_change < out_len:
            looped += 1
            without_change += 1
            random.shuffle(list_of_cities)
            current = self.two_opt(list_of_cities)
            if self.total_distance(current) < best:
                without_change = 0
                best_route_multiple = current.copy()
                best = self.total_distance(best_route_multiple)
                print('Cena puta koristeci samo two optimal sa razlicitim pocetnim rutama: ',
                      best, "pokusaj: ", looped)
        return (self.create_tour(best_route_multiple), best)


tsp = TSP(100)
best_tour, best = tsp.multiple_two_opt(10)
tsp.plot_tour(best_tour, best)
 
