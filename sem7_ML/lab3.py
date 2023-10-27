import numpy as np
import pandas as pd


def predict(X_train, y_train, X_test, n_samples = 5):
    for x_test in X_test:
        dist = [np.linalg.norm(x_test - x_train) for x_train in X_train]
        k_neighbor_labels = [y_train[i] for i in np.argsort(dist)[:n_samples]]
        yield max(set(k_neighbor_labels), key = k_neighbor_labels.count)


if __name__ == '__main__':
    data = pd.read_table('input.txt', sep=',')
    X_test = data[data.columns[0:4]].loc[(data['TT'] == 'test')].values
    X_train = data[data.columns[0:4]].loc[(data['TT'] == 'train')].values
    y_train = data[data.columns[4]].loc[(data['TT'] == 'train')].values

    with open('output.txt', 'w') as f:
        f.write('\n'.join([str(e) for e in predict(X_train, y_train, X_test)]))
