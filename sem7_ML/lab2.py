from collections.abc import Generator
import numpy as np
import pandas as pd

N_FEATURES = 4


def predict(X: list[list[float]]) -> Generator[int, None, None]:
    """
    :param X: test set
    :return: class with the highest posterior probability for each elem from test set
    """
    for x in X:
        yield np.argmax([(
                np.log(priors[class_i]) +  # prior 
                np.sum(np.log(1 / np.sqrt(2 * np.pi * var[class_i]) * np.exp(-(x - mean[class_i])**2 / 2 / var[class_i])
))  # posterior (a vector of the Gaussian distribution for x)
        ) for class_i in range(n_classes)])


def main():
    data = pd.read_table('input.txt', sep=',')
    X_test = data[data.columns[0:N_FEATURES]].loc[(data['TT'] == 'test')].values
    X_train = data[data.columns[0:N_FEATURES]].loc[(data['TT'] == 'train')].values
    y_train = data[data.columns[N_FEATURES]].loc[(data['TT'] == 'train')].values

    global n_classes, mean, var, priors
    n_classes = len(set(y_train))
    mean = [[0] * n_classes] * N_FEATURES
    var = [[0] * n_classes] * N_FEATURES
    priors = [0] * n_classes

    for class_i in range(n_classes):
        X_c = X_train[y_train == class_i]
        mean[class_i] = X_c.mean(axis=0)
        var[class_i] = X_c.var(axis=0) # avg of the squared deviations from the mean
        priors[class_i] = float(len(X_c)) / len(X_train)

    with open('output.txt', 'w') as f:
        f.write('\n'.join([str(e) for e in predict(X_test)]))


if __name__ == "__main__":
    main()
