import numpy as np
import matplotlib.pyplot as plt

from lin_logistic_reg import LogisticRegression
from non_lin_logistic_reg import LogisticRegression2D, get_log_polynom_data


def linear_reg_test():
    # generate test data
    center1 = [5, 5]
    center2 = [2, 2]
    cov = [[1, 0.2], [-0.2, 1]]
    n_points = 200
    X_plus = np.random.multivariate_normal(center1, cov, n_points)
    y_plus = np.full((n_points, 1), True)
    X_minus = np.random.multivariate_normal(center2, cov, n_points)
    y_minus = np.full((n_points, 1), False)
    X = np.concatenate((X_plus, X_minus))
    y = np.concatenate((y_plus, y_minus)).ravel()

    lrgd = LogisticRegression(eta=0.05, n_iter=500, random_state=1)
    lrgd.fit(X_train=X[(y == 0) | (y == 1)], y_train=y[(y == 0) | (y == 1)])

    # plot decisions regions
    resolution = 0.02
    x1_min, x1_max = X[:, 0].min(), X[:, 0].max()
    x2_min, x2_max = X[:, 1].min(), X[:, 1].max()
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = lrgd.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for cl in np.unique(y):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], label=cl)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

def non_linear_reg_test():
    # generate test data
    X_2, y_2 = get_log_polynom_data(params=(0.1, 0.2, 0.3, 0.4, 0.5))

    X_train = X_2[(y_2 == 0) | (y_2 == 1)]
    y_train = y_2[(y_2 == 0) | (y_2 == 1)]

    l_r2 = LogisticRegression2D(eta=0.05, n_iter=1000, random_state=1)
    l_r2.fit(X_train, y_train)
    resolution = 0.02
    x1_min, x1_max = X_train[:, 0].min(), X_train[:, 0].max()
    x2_min, x2_max = X_train[:, 1].min(), X_train[:, 1].max()
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = l_r2.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3)

    for cl in np.unique(y_train):
        plt.scatter(x=X_train[y_train == cl, 0], y=X_train[y_train == cl, 1], label=cl)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
    print(l_r2)

if __name__ == '__main__':
    linear_reg_test()
    non_linear_reg_test()

