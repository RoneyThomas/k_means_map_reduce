from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


class KMeans:

    def __init__(self, file):
        self.file_name = file

    # Calculates Ecludian Distance
    def dist(self, a, b, ax=1):
        return np.linalg.norm(a - b, axis=ax)

    def map(self):
        # Importing the dataset
        data = pd.read_csv(f'client-upload/{self.file_name}.csv')
        # Printing the dataframe
        data.head()
        # Getting the values of height and weight in respective list
        height = data['height'].values
        weight = data['weight'].values
        # Creating numpy array from the list
        X = np.array(list(zip(height, weight)))
        return X
        # plt.scatter(height, weight, c='black', s=7)

    def reduce(self, X):
        # Number of clusters
        k = 3
        # Read starting centroid values
        starting_centroids = pd.read_csv('centroids.csv')
        # X coordinates from centroids.csv
        C_x = starting_centroids.iloc[:, 0]
        # Y coordinates from centroids.csv
        C_y = starting_centroids.iloc[:, 1]
        C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
        print("Initial Centroids")
        print(C)
        # Plotting along with the Centroids
        # plt.scatter(f1, f2, c='#050505', s=7)
        # plt.scatter(C_x, C_y, marker='*', s=200, c='g')
        # plt.show()
        # To store the value of centroids when it updates
        c_old = np.zeros(C.shape)
        # Cluster Lables(0, 1, 2)
        clusters = np.zeros(len(X))
        # Error func. - Distance between new centroids and old centroids
        error = self.dist(C, c_old, None)
        # Loop will run till the error becomes zero
        while error != 0:
            # Assigning each value to its closest cluster
            for i in range(len(X)):
                distances = self.dist(X[i], C)
                cluster = np.argmin(distances)
                clusters[i] = cluster
            # Storing the old centroid values
            c_old = deepcopy(C)
            # Finding the new centroids by taking the average value
            vals_to_disk = {}
            for i in range(k):
                points = [X[j] for j in range(len(X)) if clusters[j] == i]
                vals_to_disk[i] = points
                C[i] = np.mean(points, axis=0)
            # Euclidean Distance Caculator
            error = self.dist(C, c_old, None)
            out_df = pd.concat({k: pd.Series(v) for k, v in vals_to_disk.items()})
            out_df.to_csv(f'static/graphs/{self.file_name}.csv')
            maxcount = max(len(v) for v in vals_to_disk.values())
            most_occuring = [k for k, v in vals_to_disk.items() if len(v) == maxcount]
            new_file = open(f'static/graphs/{self.file_name}.txt', mode="w", encoding="utf-8")
            new_file.write(','.join(map(repr, most_occuring)))
            new_file.close()
        return C, clusters, k

    def generate(self):
        plt.style.use('ggplot')

        X = self.map()
        self.reduce(X)
        C, clusters, k = self.reduce(X)

        colors = ['r', 'g', 'b', 'y', 'c', 'm']
        fig, ax = plt.subplots()
        for i in range(k):
            points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
            ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')
        plt.savefig(f'static/graphs/{self.file_name}.png')
