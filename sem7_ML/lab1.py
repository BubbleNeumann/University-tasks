import numpy as np

x_train_set = []
y_train_set = []
test_set = []
y_binar = []
x_tr = []

# parse file
with open('input.txt', 'r') as inp:
    lines = inp.readlines()
    for line in lines[1:]:
        line_list = line.split(',')
        if line_list[-1] == 'train\n':
            y_binar.append(int(line_list[4]))
            x_tr.append(line_list[:-2])
            if line_list[-2] == '0':
                x_train_set.append(line_list[:-2])
            else:
                y_train_set.append(line_list[:-2])
        else:
            test_set.append(line_list[:-2])

def convert_matr_to_float(matr) -> list[list[float]]:
    """
    cast initial matrix to a matrix of floats
    """
    return [[float(e) for e in row] for row in matr]


X = convert_matr_to_float(x_tr)

def sigmoid(z) -> float | None:
    try:
        return 1/(1 + np.exp(-z)) # probability measure
    except:
        print(f'sigmoid exc: z={z}')

def prediction_search(x, w, b):
    """
    weight & transform to probability measure: pass args to sigmoid func.
    """
    return sigmoid(np.dot(np.reshape(w,(1, OBJ_SIZE)), np.reshape(x,(OBJ_SIZE, 1))) + b)


def loss_function(y_true, y_pred):
    """
    loss minimization func.
    :param y_true: actual value
    :param y_pred: prediction. scope = [0,1]
    """
    loss_rezult = 0
    for i in range(len(y_true)):
        y_tru_i = y_true[i]
        y_pred_i = y_pred[i]
        loss_rezult += (-y_tru_i*np.log(y_pred_i) - (1 - y_tru_i)*np.log(1 - y_pred_i))
    return(loss_rezult/len(y_true))

OBJ_SIZE = len(X[0])

class Logistic_Regression:
    def __init__(self):
        self.w = np.random.randn(OBJ_SIZE, 1)*0.001 # weight
        self.b = np.random.randn()*0.001 # offset
        self.report = 100 # every self.report steps check the loss in train cycle

    def train(self, X, Y, regression_step = 0.005, iters = 40):
        self.loss_train = []
        self.loss_test = [] 

        for i in range(iters):
            # init derivatives as lists of zeros and a zero correspondingly
            d_w = np.zeros((OBJ_SIZE, 1))
            d_b = 0

            for j in range(len(X)):
                # calc weight & sigmoid
                z = np.dot(np.reshape(self.w,(1, OBJ_SIZE)), np.reshape(X[j],(OBJ_SIZE, 1))) + self.b
                a = sigmoid(z)

                d_w += (a - Y[j]) * np.reshape(X[j], (OBJ_SIZE, 1))
                d_b += a - Y[j]

            # normalize derivatives
            d_w /= len(X)
            d_b /= len(X)

            # gradient step
            self.w = self.w - regression_step * d_w
            self.b = self.b - regression_step * d_b

            if i % self.report == 0:
                self.loss_train.append(loss_function(Y,self.pred(X)))


    def pred(self, X):
        return np.array([prediction_search(x, self.w, self.b)[0][0] for x in X])

def main():
    log_reg = Logistic_Regression()
    log_reg.train(X, y_binar, iters=200)
    # prediction_rezult = np.array(log_reg.pred(X))
    # accuracy = np.sum((prediction_rezult > 0.5) == y_binar)/len(prediction_rezult)

    x_test = convert_matr_to_float(test_set)

    arr = [prediction_search(e, log_reg.w, log_reg.b[0][0]) for e in x_test]

    with open('output.txt','w') as f:
        f.write('\n'.join([str(1 if e is not None and e > 0.5 else 0) for e in arr]))


if __name__ == '__main__':
    main()

