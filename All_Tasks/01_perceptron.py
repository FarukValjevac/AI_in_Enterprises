#!/usr/bin/env python3

"""01_perceptron

:author:    wolf
:created:   2019.04.23
"""

import numpy as np
import matplotlib.pyplot as plt
import random

_DEBUG = False


class Perceptron():
    """Perceptron

    A simple perceptron that classifies input vectors

    fit(Mplus, Mminus, [w]:     fits the training vectors and returns a weight vector
    test(Mtest):                tests a sample against the trained weight vector
    """

    def __init__(self, weight=None):
        """Initializes the Perceptron

        :param weight:      if set, the weight vector gets stored
        """

        if weight:
            self.weight = weight

    def fit(self, Mplus, Mminus, w=None):
        """Fits the weight vector to positive and negative samples

        :param Mplus:       positive samples
        :param Mminus:      negative samples
        :param w:           optional: weight
        """

        if not w:
            w = self.weight
        else:
            print(w)
            self.weight = w
        ############################
        # TODO: HERE COMES YOUR CODE
        # Your task is to update the weight so that the fit function learns patterns

        w_tmp = []
        # Create a new weight matrix "w" with random small values needed for
        # activations and weight update
        for i in w:
            w_tmp.append(random.uniform(0, 0.01))
        w = np.asmatrix(w_tmp)

        # X = observations
        X = np.concatenate((Mplus, Mminus), axis=0)

        # y = target
        y = []

        for i in range(len(Mplus)):
            y.append(1)
        for i in range(len(Mminus)):
            y.append(0)

        y = np.asarray(y)

        # The learning rate determines how much it shifts its aim towards the missed target
        learning_rate = 0.0001
        epochs = 1000
        for epoch in range(epochs):
            activations = np.dot(X, w.T) + w.T[0]
            predictions = []
            # Wherever activations is larger than 0 predictions will get the values 1, and values 0 otherwise
            for activation in activations:
                if activation > 0:
                    predictions.append(1)
                else:
                    predictions.append(0)
            error = np.asmatrix(y - predictions)
            # Stochastic Gradient Descent
            w += learning_rate * error * X

        w = tuple(w.tolist()[0])
        # TODO: END OF YOUR CODE
        self.weight = w
        return w

    def test(self, Mtest):
        """Tests the test sample against weight vector

        :param Mtest:       test sample
        """

        w = self.weight
        return 'positive' if np.matmul(Mtest, w) > 0 else 'negative'


if __name__ == '__main__':
    Mplus = np.array([(0, 1.8), (2, 0.6)])
    Mminus = np.array([(-1.2, 1.4), (0.4, -1)])
    w = (1, 1)

    p1 = Perceptron(w)

    w = p1.fit(Mplus, Mminus, w)
    print('Weight vector w:', w)

    T = (-0.5, 2.0)
    #  test = 'positiv' if np.matmul(T, w) > 0 else 'negative'
    print('Point: ', T, 'is', p1.test(T))

    Mplus = np.array([
        (1, 1, 1, 1, 1,
         1, 0, 0, 0, 1,
         1, 0, 0, 0, 1,
         1, 0, 0, 0, 1,
         1, 1, 1, 1, 1),
        (0, 0, 0, 0, 0,
         0, 1, 1, 1, 0,
         0, 1, 0, 1, 0,
         0, 1, 1, 1, 0,
         0, 0, 0, 0, 0),
        (1, 0, 0, 0, 1,
         1, 0, 0, 0, 1,
         1, 0, 0, 0, 1,
         1, 0, 0, 0, 1,
         1, 1, 1, 1, 1)
    ])
    Mminus = np.array([
        (1, 0, 0, 0, 1,
         0, 1, 0, 1, 0,
         0, 0, 1, 0, 0,
         0, 1, 0, 1, 0,
         1, 0, 0, 0, 1),
        (0, 0, 1, 0, 0,
         0, 0, 1, 0, 0,
         1, 1, 1, 1, 1,
         0, 0, 1, 0, 0,
         0, 0, 1, 0, 0),
        (1, 1, 1, 1, 1,
         0, 0, 1, 0, 0,
         0, 0, 1, 0, 0,
         0, 0, 1, 0, 0,
         0, 0, 1, 0, 0)
    ])
    Mtest = np.array([
        (1, 1, 1, 1, 1,
         1, 0, 0, 0, 1,
         0, 1, 1, 1, 1,
         1, 0, 0, 0, 1,
         1, 1, 1, 1, 1)
    ])

    Mtest2 = np.array([
        (0, 0, 1, 0, 0,
         0, 0, 1, 0, 0,
         1, 1, 1, 1, 1,
         0, 0, 1, 0, 0,
         0, 0, 1, 0, 0)
    ])

    w = (0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0, 0)

    p2 = Perceptron()
    w = p2.fit(Mplus, Mminus, w)
    print('Weight vector w:', w)

    print('Figure: ', Mtest, 'is', p2.test(Mtest))
    result_1 = p2.test(Mtest)
    print('Figure: ', Mtest2, 'is', p2.test(Mtest2))
    result_2 = p2.test(Mtest2)

    plt.rcParams['figure.figsize'] = [10, 10]
    plt.subplot(331)
    plt.imshow(Mplus[0].reshape(5, 5), cmap='gray')
    plt.subplot(332)
    plt.imshow(Mplus[1].reshape(5, 5), cmap='gray')
    plt.subplot(333)
    plt.imshow(Mplus[2].reshape(5, 5), cmap='gray')
    plt.subplot(334)
    plt.imshow(Mminus[0].reshape(5, 5), cmap='gray')
    plt.subplot(335)
    plt.imshow(Mminus[1].reshape(5, 5), cmap='gray')
    plt.subplot(336)
    plt.imshow(Mminus[2].reshape(5, 5), cmap='gray')
    wanted = plt.subplot(337)
    wanted.title.set_text(result_1)
    plt.imshow(Mtest[0].reshape(5, 5), cmap='BuPu')
    wanted = plt.subplot(339)
    wanted.title.set_text(result_2)
    plt.imshow(Mtest2[0].reshape(5, 5), cmap='BuPu')
    plt.show()