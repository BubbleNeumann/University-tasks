import numpy as np


class LogisticRegression(object):
    def __init__(self, eta=0.05, n_iter=100, random_state=1):
        self.w_: list
        self.cost_ = []
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X_train, y_train):
        """
        Train the model using logistic regression to optimize
        the coefficients w_ by minimizing the cost function.
        :param X_train: Training input samples.
        :param y_train: Target values for the training samples.
        """
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X_train.shape[1])
        for _ in range(self.n_iter):
            output = 1. / (1. + np.exp(-np.clip(np.dot(X_train, self.w_[1:]) + self.w_[0], -250, 250)))
            errors = (y_train - output)
            self.w_[1:] += self.eta * X_train.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = -y_train.dot(np.log(output)) - ((1 - y_train).dot(np.log(1 - output)))
            self.cost_.append(cost)

        return self

    def predict(self, X):
        return np.where(np.dot(X, self.w_[1:]) + self.w_[0] >= 0.0, 1, 0)
