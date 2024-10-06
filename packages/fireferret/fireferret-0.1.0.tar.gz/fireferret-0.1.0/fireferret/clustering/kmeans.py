import matplotlib.pyplot as plt
import numpy as np

from ..utils.logger import logger


class KMeans:
    EPSILON = 0.001

    def __init__(self, n_clusters: int, max_iterations: int = 100):
        """
        Initializes the clustering algorithm with the specified number of clusters and maximum iterations.
        """
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations

    def initialize_centroids(self, X: np.ndarray):
        """
        Pick random n_cluster centroids.
        """
        random_centroids = np.random.choice(X.shape[0], size=self.n_clusters, replace=False)
        centroids = X[random_centroids]
        return centroids

    def fit(self, X: np.ndarray, animate: bool = False) -> tuple[list[list[np.ndarray]], np.ndarray]:
        """
        Take MxN matrix, where M is the number of datapoints, and N is the dimension of the vector space, and
        perform the K-means algorithm to clusterize the datapoints in distinct clusters.
        """
        if animate and X.shape[1] == 2:
            plt.ion()  # Turn on interactive mode
            self.fig, self.ax = plt.subplots()
        centroids = self.initialize_centroids(X)
        clusters = []
        for i in range(self.max_iterations):
            clusters = [[] for _ in range(self.n_clusters)]  # initialize empty clusters
            for point in X:
                distance_to_centroid = [np.linalg.norm(point - centroid) for centroid in centroids]
                cluster_assignment = np.argmin(distance_to_centroid)  # find the index of the centroid nearest to the point
                clusters[cluster_assignment].append(point)
            # assign a new centroid as the mean of the points of a cluster
            new_centroids = np.array([np.mean(cluster, axis=0) for cluster in clusters])
            if np.linalg.norm(new_centroids - centroids) < self.EPSILON:
                logger.debug(f"Converged in {i} iterations!")
                centroids = new_centroids
                break
            centroids = new_centroids
            if animate and X.shape[1] == 2:
                self.animation(clusters, centroids)
        return clusters, centroids

    def animation(self, clusters, centroids):
        plt.cla()
        for cluster, centroid in zip(clusters, centroids):
            cluster = np.array(cluster)
            self.ax.plot(cluster[:, 0], cluster[:, 1], "*", markersize=10)
            self.ax.plot(centroid[0], centroid[1], "xb", markersize=15)
        plt.grid()
        plt.show()
        plt.pause(1)
