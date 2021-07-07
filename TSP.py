import numpy as np
import operator
import matplotlib.pyplot as plt
import random as r


class Genetic:
    def __init__(self, no_of_nodes, dists_matrix, coordinates, pop, rate):
        self.N = no_of_nodes
        self.points = [str(i + 1) for i in range(no_of_nodes)]
        self.coordinates = coordinates
        self.pop = pop
        self.mu_rate = rate
        self.distance_matrix = np.array(dists_matrix).reshape((no_of_nodes, no_of_nodes))

        self.population = []
        self.best_route = ''
        self.best_route_distance = 0

    def initial_population(self):
        pops = []
        cities = []
        for i in self.points:
            cities.append(i)
        for i in range(self.pop):
            r.shuffle(cities)
            pops.append(''.join(cities))
        self.population = pops

    def calculate_route_distance(self, route):
        dist = 0
        for i in range(len(route) - 1):
            dist += self.distance_matrix[int(route[i + 1]) - 1][int(route[i]) - 1]

        dist += self.distance_matrix[int(route[-1]) - 1][int(route[0]) - 1]
        return dist

    def route_distances(self, routes):
        distances = [self.calculate_route_distance(route) for route in routes]
        return distances

    def mutate(self, route):
        r_list = []
        for i in route:
            r_list.append(i)

        for i in range(self.N):
            if np.random.rand() < self.mu_rate:
                i1 = np.random.randint(self.N)
                i2 = np.random.randint(self.N)
                r_list[i1], r_list[i2] = r_list[i2], r_list[i1]
        return ''.join(r_list)

    def mutation(self, routes):
        mutated_routes = [self.mutate(route) for route in routes]
        return mutated_routes

    def crossover(self, routes):
        for i in range(len(routes)):
            route1 = routes[np.random.randint(self.pop)]
            route2 = routes[np.random.randint(self.pop)]
            a = np.random.randint(self.N)
            b = np.random.randint(self.N)
            start = min([a, b])
            end = max([a, b])
            new_route = route1[start:end]
            for j in route2:
                if j not in new_route:
                    new_route = new_route + j
            routes[i] = new_route
        return routes

    def repeat_crossover_and_mutation(self):
        routes_distances = self.route_distances(self.population)
        best_route_distance = min(routes_distances)
        best_route = self.population[operator.indexOf(routes_distances, best_route_distance)]
        for i in range(500):
            self.population = self.crossover(self.population)
            self.population = self.mutation(self.population)
            routes_distances = self.route_distances(self.population)
            if min(routes_distances) < best_route_distance:
                best_route_distance = min(routes_distances)
                best_route = self.population[operator.indexOf(routes_distances, best_route_distance)]

        self.best_route_distance = best_route_distance
        self.best_route = best_route

    def show_best_route_and_distance(self):
        route = [r for r in self.best_route]
        route.append(self.best_route[0])
        br = ' -> '.join(route)
        print(f"Best route is: {br} and shortest distance is {self.best_route_distance}")
        x_coords = []
        y_coords = []
        for i in route:
            x_coords.append(self.coordinates[i][0])
            y_coords.append(self.coordinates[i][1])
        plt.plot(x_coords, y_coords, 'b-o')
        plt.title(f'best route distance is {self.best_route_distance} km')
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        for point, coordinate in self.coordinates.items():
            plt.annotate(point, coordinate, color='red', ha='center', va='bottom')
        plt.savefig('path.png')


N = 7
pop = 500
mu_rate = 0.01

dists = [float('inf'), 12, 10, float('inf'), float('inf'), float('inf'), 12,
         12, float('inf'), 8, 12, float('inf'), float('inf'), float('inf'),
         10, 8, float('inf'), 11, 3, float('inf'), 9,
         float('inf'), 12, 11, float('inf'), 11, 10, float('inf'),
         float('inf'), float('inf'), 3, 11, float('inf'), 6, 7,
         float('inf'), float('inf'), float('inf'), 10, 6, float('inf'), 9,
         12, float('inf'), 9, float('inf'), 7, 9, float('inf')]

coordinates = {
    '7': (20, 20),
    '5': (30, 30),
    '3': (18, 35),
    '1': (-20, 33),
    '2': (-10, 50),
    '4': (50, 40),
    '6': (70, 25),
}

gen = Genetic(no_of_nodes=7, dists_matrix=dists, coordinates=coordinates, pop=500, rate=0.01)
gen.initial_population()
gen.repeat_crossover_and_mutation()
gen.show_best_route_and_distance()
