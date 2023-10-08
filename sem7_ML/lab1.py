import numpy as np


def read_file(file_path: str):
    y = []
    x_train = []
    x_test = []
    with open(file_path, 'r') as inp:
        lines = inp.readlines()
        for l in lines[1:]:
            line_list = l.split(',')
            if line_list[-1] == 'train\n':
                y.append(int(line_list[4]))
                x_train.append(line_list[:-2])
            else:
                x_test.append(line_list[:-2])
        return y, x_test, x_train


def sigmoid(z: float) -> float:
    """
    transforms a number to a probability measure
    """
    return 1 / (1 + np.exp(-z))


def calc_loss(y_true: list[float], y_pred: list[float]):
    """
    logistic loss minimization func. Li(a)=-yi-log(a)-(1-yi)*log(1-a)
    :param y_true: actual value
    :param y_pred: prediction. scope = [0,1]
    """
    return sum([-y_true[i] * np.log(y_pred[i]) - (1 - y_true[i]) * np.log(1 - y_pred[i]) for i in range(len(y_true))]) / len(y_true)


class Logistic_Regression:
    def __init__(self, obj_size: int):
        self.obj_size = obj_size
        self.w = np.random.randn(obj_size, 1) * 0.001 # weight
        self.b = np.random.randn() * 0.001 # offset

    def train(self, X: list[list[float]], Y: list[float], learning_rate = 0.005, epochs = 40) -> None:
        """
        :param X: training set
        :param Y: 
        :param learning_rate: gradient step
        :param epochs: number of iterations over the dataset
        """
        for _ in range(epochs):
            d_w = np.zeros((self.obj_size, 1))
            d_b = 0

            for j in range(len(X)):
                # calc weight & sigmoid (make the prediction)
                z = np.dot(np.reshape(self.w,(1, self.obj_size)), np.reshape(X[j],(self.obj_size, 1))) + self.b
                a = sigmoid(z)

                d_w += (a - Y[j]) * np.reshape(X[j], (self.obj_size, 1))
                d_b += a - Y[j]

            d_w /= len(X)
            d_b /= len(X)

            # gradient step (minimize the loss step by step)
            self.w -= learning_rate * d_w
            self.b -= learning_rate * d_b

    def predict(self, x: list[float]) -> float:
        """
        weight & transform to probability measure: pass args to sigmoid func.
        """
        return sigmoid(np.dot(np.reshape(self.w, (1, self.obj_size)), np.reshape(x, (self.obj_size, 1))) + self.b)


def main():
    y, x_test, x_train = read_file(file_path='input.txt')
    x_train = [[float(e) for e in row] for row in x_train]

    log_reg = Logistic_Regression(obj_size=len(x_train[0]))
    log_reg.train(X=x_train, Y=y, epochs=200)

    x_test = [[float(e) for e in row] for row in x_test]

    prediction = [log_reg.predict(e) for e in x_test]

    with open('output.txt','w') as f:
        f.write('\n'.join([str(1 if e is not None and e > 0.5 else 0) for e in prediction]))


if __name__ == '__main__':
    main()

