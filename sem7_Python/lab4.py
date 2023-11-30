import random

import matplotlib.pyplot as plt
import numpy as np


def sample_clusters(n_clusters: int, n_points=500, random_state=42):
    from sklearn.datasets import make_blobs
    centers = [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(n_clusters)]
    coefs = [[random.uniform(0, 2)] for _ in range(n_clusters)]
    data, labels = make_blobs(n_points, centers=centers, cluster_std=coefs, random_state=random_state)
    return data, labels


class KMeans:
    def __init__(self, k, max_iters=100):
        self.n_clusters = k
        self.max_iters = max_iters

    def fit(self, X) -> (dict, np.ndarray):
        """

        :param X:
        :return:
        """
        self.centroids = self._init_centroids(X)
        for _ in range(self.max_iters):
            clusters = self._create_clusters(X, self.centroids)
            self.centroids = self._calc_centroids(clusters)

        return clusters, self.centroids

    def _init_centroids(self, X: np.ndarray) -> np.ndarray:
        """
        init centroids randomly
        """
        indices = random.sample(range(len(X)), self.n_clusters)
        return np.array([X[i] for i in indices])

    def _create_clusters(self, X: np.ndarray, centroids: np.ndarray) -> dict:
        """
        assign data points to the nearest centroids to create clusters.
        :param X:
        :param centroids:
        :return: A dictionary with cluster indices as keys and lists of data points as values.
        """
        clusters = {i: [] for i in range(self.n_clusters)}

        for point in X:
            distances = [np.sqrt(np.sum((point - centroid) ** 2)) for centroid in centroids]
            closest_centroid_index = np.argmin(distances)
            clusters[closest_centroid_index].append(point)

        return clusters

    def _calc_centroids(self, clusters: dict) -> np.ndarray:
        """
        calc new centroids based on the mean of the data points in each cluster.
        :param clusters: A dictionary with cluster indices as keys and lists of data points as values.
        :return: Updated centroids after re-calculation.
        """
        centroids = np.zeros((self.n_clusters, len(clusters[0][0])))
        for i, cluster in clusters.items():
            cluster_mean = np.mean(cluster, axis=0)
            centroids[i] = cluster_mean

        return centroids


if __name__ == "__main__":
    n_clusters = 4
    data, labels = sample_clusters(n_clusters)
    kmeans = KMeans(k=n_clusters)
    clusters, centroids = kmeans.fit(data)

    for i, cluster in clusters.items():
        print(f"Cluster {i + 1} has {len(cluster)} points")

    plt.scatter(*data.T, c=labels, cmap='viridis', s=50)
    plt.scatter(*centroids.T, marker='o', s=150, c='k', edgecolors='w')
    plt.show()
