from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


class KMeans:

    def __init__(self, file):
        self.file_name = file

    def generate(self):
        plt.style.use('ggplot')

        # Importing the dataset
        data = pd.read_csv(f'client-upload/{self.file_name}.csv')
        print("Input Data and Shape")
        print(data.shape)
        data.head()

        # Getting the values and plotting it
        f1 = data['height'].values
        f2 = data['weight'].values
        X = np.array(list(zip(f1, f2)))
        plt.scatter(f1, f2, c='black', s=7)

        # Euclidean Distance Caculator
        def dist(a, b, ax=1):
            return np.linalg.norm(a - b, axis=ax)

        # Number of clusters
        k = 3
        # Read starting centroid values
        startingCentroids = pd.read_csv('centroids.csv')
        # X coordinates of random centroids
        C_x = startingCentroids.iloc[:, 0]
        # Y coordinates of random centroids
        C_y = startingCentroids.iloc[:, 1]
        C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
        print("Initial Centroids")
        print(C)
        print(startingCentroids['height'].values.tolist())

        # Plotting along with the Centroids
        plt.scatter(f1, f2, c='#050505', s=7)
        plt.scatter(C_x, C_y, marker='*', s=200, c='g')
        # plt.show()

        # To store the value of centroids when it updates
        C_old = np.zeros(C.shape)
        # Cluster Lables(0, 1, 2)
        clusters = np.zeros(len(X))
        # Error func. - Distance between new centroids and old centroids
        error = dist(C, C_old, None)
        # Loop will run till the error becomes zero
        while error != 0:
            # Assigning each value to its closest cluster
            for i in range(len(X)):
                distances = dist(X[i], C)
                cluster = np.argmin(distances)
                clusters[i] = cluster
            # Storing the old centroid values
            C_old = deepcopy(C)
            # Finding the new centroids by taking the average value
            for i in range(k):
                points = [X[j] for j in range(len(X)) if clusters[j] == i]
                C[i] = np.mean(points, axis=0)
            error = dist(C, C_old, None)

        colors = ['r', 'g', 'b', 'y', 'c', 'm']
        fig, ax = plt.subplots()
        for i in range(k):
            points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
            ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')
        plt.savefig(f'graphs/{self.file_name}.png')
