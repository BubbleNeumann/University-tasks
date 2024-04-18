from __future__ import annotations

from typing import TYPE_CHECKING

from builtins import object
import numpy as np

from ..layers import *
from ..layer_utils import *

if TYPE_CHECKING:
    from typing import List, Optional


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecure should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(
        self,
        input_dim: int = 3 * 32 * 32,
        hidden_dim: int = 100,
        num_classes: int = 10,
        weight_scale: float = 1e-3,
        reg: float = 0.0,
    ):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {}
        self.reg = reg

        ############################################################################
        # TODO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian centered at 0.0 with               #
        # standard deviation equal to weight_scale, and biases should be           #
        # initialized to zero. All weights and biases should be stored in the      #
        # dictionary self.params, with first layer weights                         #
        # and biases using the keys 'W1' and 'b1' and second layer                 #
        # weights and biases using the keys 'W2' and 'b2'.                         #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        W1 = np.random.randn(input_dim, hidden_dim) * weight_scale
        self.params["W1"] = W1

        b1 = np.zeros(hidden_dim)
        self.params["b1"] = b1

        W2 = np.random.randn(hidden_dim, num_classes) * weight_scale
        self.params["W2"] =W2

        b2 = np.zeros(num_classes)
        self.params["b2"] = b2

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

    def loss(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the two-layer net, computing the    #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        fc_layer1, cache1 = affine_relu_forward(X, self.params["W1"], self.params["b1"])
        scores, cache2 = affine_forward(fc_layer1, self.params["W2"], self.params["b2"])

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the two-layer net. Store the loss  #
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        score_loss, dscores = softmax_loss(scores, y)

        reg_loss = 0
        reg_loss += np.sum(np.square(self.params["W1"]))
        reg_loss += np.sum(np.square(self.params["W2"]))

        loss = score_loss + 0.5 * self.reg * reg_loss


        dout_1, dW2, db2 = affine_backward(dscores, cache2)
        dX, dW1, db1 = affine_relu_backward(dout_1, cache1)

        grads["W1"] = dW1 + self.reg * self.params['W1']
        grads["b1"] = db1
        grads["W2"] = dW2 + self.reg * self.params['W2']
        grads["b2"] = db2


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch/layer normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch/layer norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch/layer normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(
        self,
        hidden_dims: List[int],
        input_dim: int = 3 * 32 * 32,
        num_classes: int = 10,
        dropout: int = 1,
        normalization: Optional[str] = None,
        reg: float = 0.0,
        weight_scale: float = 1e-2,
        dtype=np.float32,
        seed: Optional[int] = None,
    ):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=1 then
          the network should not use dropout at all.
        - normalization: What type of normalization the network should use. Valid values
          are "batchnorm", "layernorm", or None for no normalization (the default).
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.normalization = normalization
        self.use_dropout = dropout != 1
        self.reg = reg
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution centered at 0 with standard       #
        # deviation equal to weight_scale. Biases should be initialized to zero.   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to ones and shift     #
        # parameters should be initialized to zeros.                               #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
       

        for layer_index in range(self.num_layers):
            # Проверяем, не является ли текущий слой последним
            if layer_index != self.num_layers - 1:
                # Если это не первый слой, инициализируем веса с предыдущего слоя
                if layer_index == 0:
                    weights = np.random.normal(loc=0.0, scale=weight_scale, size=(input_dim, hidden_dims[0]))
                else:
                    weights = np.random.normal(loc=0.0, scale=weight_scale, size=(hidden_dims[layer_index - 1], hidden_dims[layer_index]))
                # Инициализируем смещения нулями
                biases = np.zeros(hidden_dims[layer_index])

                # Если используется нормализация по батчу или слойная нормализация
                if self.normalization in ["batchnorm", "layernorm"]:
                    # Инициализируем параметры гамма и бета
                    self.params[f"gamma{str(layer_index + 1)}"] = np.ones(hidden_dims[layer_index])
                    self.params[f"beta{str(layer_index + 1)}"] = np.zeros(hidden_dims[layer_index])
            else:
                # Для последнего слоя инициализируем веса для выходных классов
                weights = np.random.normal(loc=0.0, scale=weight_scale, size=(hidden_dims[-1], num_classes))
                # Инициализируем смещения нулями
                biases = np.zeros(num_classes)

            # Сохраняем веса и смещения в параметры модели
            self.params[f"W{str(layer_index + 1)}"] = weights
            self.params[f"b{str(layer_index + 1)}"] = biases


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {"mode": "train", "p": dropout}
            if seed is not None:
                self.dropout_param["seed"] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.normalization == "batchnorm":
            self.bn_params = [{"mode": "train"} for i in range(self.num_layers - 1)]
        if self.normalization == "layernorm":
            self.bn_params = [{} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = "test" if y is None else "train"

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param["mode"] = mode
        if self.normalization == "batchnorm":
            for bn_param in self.bn_params:
                bn_param["mode"] = mode
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        caches = {}

        for i in range(self.num_layers - 1):
            w_i_str = f"W{str(i + 1)}"
            b_i_str = f"b{str(i + 1)}"

            if i == 0:
                out_ = X

            # Если используется пакетная нормализация
            if self.normalization == "batchnorm":
                fc_out, fc_cache = affine_forward(out_, self.params[w_i_str], self.params[b_i_str])
                bn_out, bn_cache = batchnorm_forward(fc_out, self.params[f"gamma{str(i + 1)}"], self.params[f"beta{str(i + 1)}"], self.bn_params[i])
                out_, relu_cache = relu_forward(bn_out)
                caches[i + 1] = (fc_cache, bn_cache, relu_cache)

            # Если используется нормализация по слоям
            elif self.normalization == "layernorm":
                fc_out, fc_cache = affine_forward(out_, self.params[w_i_str], self.params[b_i_str])
                ln_out, ln_cache = layernorm_forward(fc_out, self.params[f"gamma{str(i + 1)}"], self.params[f"beta{str(i + 1)}"], self.ln_params[i])
                out_, relu_cache = relu_forward(ln_out)
                caches[i + 1] = (fc_cache, ln_cache, relu_cache)

            # Если не используется нормализация
            else:
                out_, caches[i + 1] = affine_relu_forward(out_, self.params[w_i_str], self.params[b_i_str])

            # Если используется dropout
            if self.use_dropout:
                # Применение dropout к выходу текущего слоя
                out_, caches[f"dropout{str(i + 1)}"] = dropout_forward(out_, self.dropout_param)

        scores, caches[self.num_layers] = affine_forward(out_, self.params[f"W{str(self.num_layers)}"], self.params[f"b{str(self.num_layers)}"])
        

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == "test":
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch/layer normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Рассчитываем softmax loss и его градиенты
        loss, dscores = softmax_loss(scores, y)
        
        # Обратный проход по сети
        for i in range(self.num_layers, 0, -1):
            # Добавляем регуляризацию к loss
            loss += 0.5 * self.reg * np.sum(np.square(self.params[f"W{str(i)}"]))
        
            if i == self.num_layers:
                # Обратный проход для последнего слоя
                dout, grads[f"W{str(i)}"], grads[f"b{str(i)}"] = affine_backward(dscores, caches[i])
            else:
                # Если используется dropout, применяем его в обратном направлении
                if self.use_dropout:
                    dout = dropout_backward(dout, caches[f"dropout{str(i)}"])
        
                if self.normalization == "batchnorm":
                    # Обратный проход для слоя batch normalization
                    fc_cache, bn_cache, relu_cache = caches[i]
                    dbn_out = relu_backward(dout, relu_cache)
                    dfc_out, grads[f"gamma{str(i)}"], grads[f"beta{str(i)}"] = batchnorm_backward(dbn_out, bn_cache)
                    dout, grads[f"W{str(i)}"], grads[f"b{str(i)}"] = affine_backward(dfc_out, fc_cache)
        
                elif self.normalization == "layernorm":
                    # Обратный проход для слоя layer normalization
                    fc_cache, ln_cache, relu_cache = caches[i]
                    dln_out = relu_backward(dout, relu_cache)
                    dfc_out, grads[f"gamma{str(i)}"], grads[f"beta{str(i)}"] = layernorm_backward(dln_out, ln_cache)
                    dout, grads[f"W{str(i)}"], grads[f"b{str(i)}"] = affine_backward(dfc_out, fc_cache)
        
                else:
                    # Обратный проход для слоя активации ReLU и аффинного слоя
                    dout, grads[f"W{str(i)}"], grads[f"b{str(i)}"] = affine_relu_backward(dout, caches[i])
        
            # Добавляем регуляризацию градиентам весов
            grads['W' + str(i)] += self.reg * self.params['W' + str(i)]
        


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads