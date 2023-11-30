import numpy as np
import random
from typing import Tuple


def ellipsoid(x, y, p):
    """
    evaluate points (x, y) in the context of an ellipsoidal boundary or surface
    :param p: parameters of the ellipsoid
    """
    return p[0] * x + p[1] * y + p[2] * x * y + p[3] * x * x + p[4] * y * y - 1


def get_log_polynom_data(params: Tuple, n_points = 3000, arg_range = 5.):
    """
    generate a dataset, with each datapoint having five features.
    labels are calculated using the ellipsoid func.
    """

    def rand_in_range(rand_range: float = 1.0) -> float:
        return random.uniform(-0.5 * rand_range, 0.5 * rand_range)

    features = np.zeros((n_points, 5), dtype=float)
    features[:, 0] = np.array([rand_in_range(arg_range) for _ in range(n_points)])
    features[:, 1] = np.array([rand_in_range(arg_range) for _ in range(n_points)])
    features[:, 2] = features[:, 0] * features[:, 1]
    features[:, 3] = features[:, 0] * features[:, 0]
    features[:, 4] = features[:, 1] * features[:, 1]
    groups = np.bool_(np.array([np.sign(ellipsoid(features[i, 0], features[i, 1], params)) * 0.5 + 0.5 for i in range(n_points)]))
    return features, groups


class LogisticRegression2D(object):
    def __init__(self, eta=0.05, n_iter=100, random_state=1):
        self.w_ = None
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.loss = 0.

    def fit(self, X_train, y_train):
        """
        - init the weights using a random normal distribution,
        - set up the input data matrix with an added bias term,
        - perform logistic regression iterations to optimize weights using gradient descent
        - enforce non-negativity to the weights.

        :param X_train: Training input samples.
        :param y_train: Target values for the training samples.
        :return: the instance of the fitted estimator.
        """
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=6)
        ones = np.ones((X_train.shape[0], 1), dtype=float)
        X_ = np.hstack((ones, X_train))

        # an iterative process for training a model, using a gradient descent,
        # where the weight vector is adjusted based on the difference between 
        # predicted and actual target values, scaled by a learning rate self.eta.

        for _ in range(self.n_iter):
            self.w_ -= self.eta * X_.T @ ((lambda z: 1. / (1. + np.exp(-z)))(X_ @ self.w_) - y_train)
            # self.loss 

        self.w_ = np.abs(self.w_)
        return self

    def net_input(self, X):
        """
        process the input features X through an ellipsoid equation
        """
        return ellipsoid(X[:, 0], X[:, 1], self.w_[1:] / self.w_[0])

    def predict(self, X):
        """
        check if the values in the net input result are >= 0
        and indicate True or False class correspondingly.
        """
        return np.where(self.net_input(X) >= 0.0, 1, 0)

    # def loss(self, groups_probs: np.ndarray, groups:np.ndarray):
    #     self.loss = (-groups * np.log(groups_probs) - (1.0 - groups) * np.log(1.0 - groups_probs)).mean()
    #     return self.loss

    def __str__(self):
        return '{' + f'\'thetas\': {self.w_[1:] / self.w_[0]}, \'loss\':{self.loss}' + '}'

