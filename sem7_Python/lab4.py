import numpy as np
from matplotlib import image as mpimg
from numpy.random import seed
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.mixture import GaussianMixture
from yellowbrick.cluster import KElbowVisualizer
from scipy.spatial.distance import cdist
import warnings
import random
from time import sleep

warnings.filterwarnings('ignore')
seed(42)

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=MEDIUM_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE)
plt.rc('axes', labelsize=SMALL_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)


#Кластеризация Kmeans
def sample_clusters(n_clusters=4, n_points=500, random_state=42):
    centers = [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(n_clusters)]
    coefs = [[random.uniform(0, 2)] for _ in range(n_clusters)]
    data, labels = make_blobs(n_samples=n_points,
                              centers=centers,
                              cluster_std=coefs,
                              random_state=random_state)
    return data, labels


#Инерция в кластерах
def inertia_plot_update(inertias, ax, delay=1):
    inertias.plot(color='k', lw=1, title='Инерция', ax=ax, xlim=(inertias.index[0], inertias.index[-1]), ylim=(0, inertias.max()))
    fig.canvas.draw()
    sleep(delay)


def plot_kmeans_result(data, labels, centroids,
                       assignments, ncluster, Z, ax):
    ax.scatter(*data.T, c=labels, s=15, cmap='viridis')

    #точки центров кластеров
    ax.scatter(*centroids.T, marker='o', c='k',
               s=200, edgecolor='w', zorder=9)
    for i, c in enumerate(centroids):

        xy = data[assignments == i]
        xy = np.c_[xy, np.full(len(xy), c[0], dtype=int)]
        xy = np.c_[xy, np.full(len(xy), c[1], dtype=int)]
        ax.plot(xy[:, [0, 2]].T, xy[:, [1, 3]].T, ls='--', color='w', lw=0.5, zorder=8)

    #области Вороного
    ax.imshow(Z, interpolation='nearest',
              extent=(xx.min(), xx.max(), yy.min(), yy.max()),
              cmap=plt.cm.viridis, aspect='auto', origin='lower', alpha=.2)
    ax.set_title('Количество кластеров: {}'.format(ncluster))
    plt.tight_layout()


#Метод локтя
n_clusters, max_clusters = 4, 7
cluster_list = list(range(1, max_clusters + 1))
inertias = pd.Series(index=cluster_list)

data, labels = sample_clusters(n_clusters=n_clusters)
x, y = data.T

xx, yy = np.meshgrid(np.arange(x.min() - 1, x.max() + 1, .01),
                     np.arange(y.min() - 1, y.max() + 1, .01))

fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(12, 8))
axes = np.array(axes).flatten()
plt.tight_layout()

#кластеры
axes[0].scatter(x, y, c=labels, s=10, cmap='viridis')
axes[0].set_title('{} образца кластеров'.format(n_clusters));

for c, n_clusters in enumerate(range(1, max_clusters + 1), 2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(data)
    centroids, assignments, inertia = kmeans.cluster_centers_, kmeans.labels_, kmeans.inertia_

    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plot_kmeans_result(data, labels, centroids, assignments, n_clusters, Z, axes[c])

visualizer = KElbowVisualizer(KMeans(), ax=axes[1], k=(1, max_clusters))
visualizer.fit(data)

plt.savefig('nclusters', dpi=300);
plt.tight_layout()


#Исследование силуэтов
def plot_silhouette(values, y_lower, i, n_cluster, ax):
    cluster_size = values.shape[0]
    y_upper = y_lower + cluster_size

    color = plt.cm.viridis(i / n_cluster)
    ax.fill_betweenx(np.arange(y_lower, y_upper), 0, values,
                     facecolor=color, edgecolor=color, alpha=0.7)
    ax.text(-0.05, y_lower + 0.5 * cluster_size, str(i))
    y_lower = y_upper + 10
    return y_lower


def format_silhouette_plot(ax):
    ax.set_title("Силуэты")
    ax.set_xlabel("Коэффициент силуэта")
    ax.set_ylabel("Номер точки")
    ax.axvline(
        x=silhouette_avg, color="red", linestyle="--", lw=1)
    ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])


def plot_final_assignments(x, y, centroids,
                           assignments, n_cluster, ax):
    c = plt.cm.viridis(assignments / n_cluster)
    ax.scatter(x, y, marker='.', s=30,
               lw=0, alpha=0.7, c=c, edgecolor='k', cmap='viridis')
    ax.scatter(*centroids.T, marker='o',
               c='w', s=200, edgecolor='k', cmap='viridis')
    for i, c in enumerate(centroids):
        ax.scatter(*c, marker='${}$'.format(i),
                   s=50, edgecolor='k', cmap='viridis')

    ax.set_title('{} кластеров'.format(n_cluster))


n_clusters = 4
max_clusters = 7
cluster_list = list(range(1, max_clusters + 1))
inertias = pd.Series(index=cluster_list)

data, labels = sample_clusters(n_clusters=n_clusters)
x, y = data.T

fig, axes = plt.subplots(ncols=2,
                         nrows=max_clusters, figsize=(12, 20))
fig.tight_layout()
axes[0][0].scatter(x, y, c=labels, s=10, cmap='viridis')
axes[0][0].set_title('Образцы кластеров')
for row, n_cluster in enumerate(range(2, max_clusters + 1), 1):
    kmeans = KMeans(n_clusters=n_cluster, random_state=42).fit(data)
    centroids, assignments, inertia = \
        kmeans.cluster_centers_, kmeans.labels_, kmeans.inertia_

    silhouette_avg = silhouette_score(data, assignments)
    silhouette_values = silhouette_samples(data, assignments)
    silhouette_plot, cluster_plot = axes[row]

    y_lower = 10
    for i in range(n_cluster):
        y_lower = plot_silhouette(np.sort(silhouette_values[assignments == i]), y_lower, i, n_cluster, silhouette_plot)
    format_silhouette_plot(silhouette_plot)
    plot_final_assignments(x, y, centroids, assignments, n_cluster, cluster_plot)
    fig.tight_layout()

# visualizer = KElbowVisualizer(KMeans(), ax=axes[0][1], k=(1, max_clusters))
# visualizer.fit(data)

img = mpimg.imread('img.png')
axes[0][1].imshow(img)

fig.suptitle('Силуэты KMeans для {} кластеров'.format(n_clusters), fontsize=14)
fig.tight_layout()
fig.subplots_adjust(top=.95)


#Модель гауссовой смеси (GMM)
#Метод локточков
n_clusters, max_clusters = 4, 7
cluster_list = list(range(1, max_clusters + 1))
inertias = pd.Series(index=cluster_list)

data, labels = sample_clusters(n_clusters=n_clusters)
x, y = data.T

xx, yy = np.meshgrid(np.arange(x.min() - 1, x.max() + 1, .01),
                     np.arange(y.min() - 1, y.max() + 1, .01))

fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(12, 8))
axes = np.array(axes).flatten()
plt.tight_layout()

#кластеры
axes[0].scatter(x, y, c=labels, s=10, cmap='viridis')
axes[0].set_title('{} образца кластеров'.format(n_clusters));

distortions = []

for c, n_clusters in enumerate(range(1, max_clusters + 1), 2):
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    assignments = gmm.fit_predict(data)
    centroids = gmm.means_
    distortions.append(sum(np.min(cdist(data, centroids, 'euclidean'), axis=1) ** 2))

    Z = gmm.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plot_kmeans_result(data, labels, centroids, assignments, n_clusters, Z, axes[c])

axes[1].plot(range(1, max_clusters + 1), distortions, 'bx-')
axes[1].set_xlabel('Количество кластеров')
axes[1].set_ylabel('Инерция')
axes[1].set_title('Метод локтя с использованием искажения')
plt.savefig('nclusters', dpi=300)
plt.tight_layout()


#Силуэты
n_clusters = 4
max_clusters = 7
cluster_list = list(range(1, max_clusters + 1))
inertias = pd.Series(index=cluster_list)

data, labels = sample_clusters(n_clusters=n_clusters)
x, y = data.T

fig, axes = plt.subplots(ncols=2,
                         nrows=max_clusters, figsize=(12, 20))
fig.tight_layout()
axes[0][0].scatter(x, y, c=labels, s=10, cmap='viridis')
axes[0][0].set_title(f'Образцы {n_clusters} кластеров')
distortions = []
for row, n_cluster in enumerate(range(2, max_clusters + 1), 1):
    gmm = GaussianMixture(n_components=n_cluster, random_state=42)
    assignments = gmm.fit_predict(data)
    centroids = gmm.means_
    distortions.append(sum(np.min(cdist(data, centroids, 'euclidean'), axis=1) ** 2))

    silhouette_avg = silhouette_score(data, assignments)
    silhouette_values = silhouette_samples(data, assignments)
    silhouette_plot, cluster_plot = axes[row]

    y_lower = 10
    for i in range(n_cluster):
        y_lower = plot_silhouette(np.sort(silhouette_values[assignments == i]), y_lower, i, n_cluster, silhouette_plot)
    format_silhouette_plot(silhouette_plot)
    plot_final_assignments(x, y, centroids, assignments, n_cluster, cluster_plot)
    fig.tight_layout()

axes[0][1].plot(range(2, max_clusters + 1), distortions, 'bx-')
axes[0][1].set_xlabel('Количество кластеров')
axes[0][1].set_ylabel('Инерция')
axes[0][1].set_title('Метод локтя с использованием искажения')
fig.suptitle('Силуэты GMM для {} кластеров'.format(n_clusters), fontsize=14)
fig.tight_layout()
fig.subplots_adjust(top=.95)
plt.show()
