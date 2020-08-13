# Kunal Mukherjee
# 2/16/2019
# CS 6375

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
import cvxopt
import math

# global variables to control the number of iterations
VERBOSE = True
ITER = 100


# the linear kernel
def linear_kernel(x, y):
    return np.dot(x, y)


class SVM:
    def __init__(self, c=0, kernel=linear_kernel):
        self.w = np.zeros(1)
        self.b = 0
        self.c = float(c)
        self.kernel = kernel

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # X =  feature(d) x samples(n)
        # P = [[x1x1y1y1 x1x2y1y2 ... x1XnY1Yn]
        #      [x2x1y2y1 x2x2y2y2 ... x2XnY2Yn]
        #      [x3x1y3y1 x3x2y3y2 ... x3Xn1Y3Yn]
        #                   :
        #      [Xnx1Yny1 Xnx2dYdy2 ... XnXnYnYn]

        # Gram matrix
        K = np.zeros((n_samples, n_samples))

        for i in range(n_samples):
            for j in range(n_samples):
                K[i, j] = self.kernel(X[i], X[j])

        # P = x^Tx
        P = cvxopt.matrix(np.outer(y, y) * K)

        # q = -1 (1 x N)
        q = cvxopt.matrix(np.ones(n_samples) * -1)

        # A = y^T
        A = cvxopt.matrix(y, (1, n_samples))

        # b = 0
        b = cvxopt.matrix(0.0)

        print(self.c)
        
        if self.c == 0:
            # G = -1 (N x N)
            G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))

            # h = 0 (1 x N)
            h = cvxopt.matrix(np.zeros(n_samples))
        else:
            temp1 = np.diag(np.ones(n_samples) * -1)
            temp2 = np.identity(n_samples)
            G = cvxopt.matrix(np.vstack((temp1, temp2)))

            temp1 = np.zeros(n_samples)
            temp2 = np.ones(n_samples) * self.c
            h = cvxopt.matrix(np.hstack((temp1, temp2)))

        cvxopt.solvers.options['show_progress'] = VERBOSE
        cvxopt.solvers.options['maxiters'] = ITER
        #cvxopt.solvers.options['abstol'] = 1e-8
        #cvxopt.solvers.options['reltol'] = 1e-7

        solution = cvxopt.solvers.qp(P, q, G, h, A, b)
        # print('sol: ', solution)

        # All the Lagrange multipliers
        lagrange_multipler = np.ravel(solution['x'])
        # print('lagrange_multipler: \n', lagrange_multipler)

        # Lagrange have non zero lagrange multiplier
        # creates a boolean array that shows
        # which Lagrange multipliers non-zero(greater than 10^-5)
        non_0_lagragnge_boolean_arr = lagrange_multipler > 1e-5
        # print('non_0_lagragnge_boolean_arr: \n', non_0_lagragnge_boolean_arr)

        # get the indices of the lagrange multiplier that are
        # non-zero(greater than 10^-5)
        non_0_lagrange_multiplier_indices = np.arange(len(lagrange_multipler))[non_0_lagragnge_boolean_arr]
        # print('non_0_lagrange_multiplier_indices: \n', non_0_lagrange_multiplier_indices)

        # get the lagrange multiplier that are
        # non-zero (greater than 10^-5)
        self.non_0_lagrange_multiplier = lagrange_multipler[non_0_lagragnge_boolean_arr]
        # print('non_0_lagrange_multiplier: \n', non_0_lagrange_multiplier)

        # support vectors are the vectors that have the lagrange multiplier
        self.support_vector = X[non_0_lagragnge_boolean_arr]
        # for i in non_0_lagrange_multiplier_indices:
        #    print('Original Support Vec', X[i])

        # support vector's classification
        self.support_vector_classfication = y[non_0_lagragnge_boolean_arr]
        # print('support_vector_classfication: \n', support_vector_classfication)

        # Weights
        self.w = np.zeros(n_features)
        for n in range(len(self.non_0_lagrange_multiplier)):
            self.w += self.non_0_lagrange_multiplier[n] *\
                    self.support_vector_classfication[n] *\
                    self.support_vector[n]

        # Intercept
        self.b = 0
        for i in non_0_lagrange_multiplier_indices:
            self.b += (1 / y[i]) - np.dot(self.w.T, X[i])
        self.b /= len(non_0_lagrange_multiplier_indices)

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def predict(self, X):
        return np.sign(self.project(X))

    def initialize_w_b(self, w, b):
        self.w = w
        self.b = b

    def update_c(self, c):
        self.c = float(c)

    def get_w_b(self):
        return self.w, self.b


def linear_kernel_SVM():
    # Open the file for writing output
    f = open("outputLinearSVM.txt", "w")

    # data loading
    spam_train = pd.read_csv("spam_train.data")
    spam_validate = pd.read_csv("spam_validation.data")
    spam_test = pd.read_csv("spam_test.data")

    # print(spam_train.shape)
    # print(spam_train.head())

    # data processing
    X_train = spam_train.drop('Y', axis=1)
    Y_train = spam_train['Y']
    Y_train = [-1 if i == 0 else i for i in Y_train]

    # data put in np array
    x_train = np.asarray(X_train)
    y_train = np.asarray([np.float64(i) for i in Y_train])

    # initialize an svm
    svm1 = SVM()

    # create a weight and bias list
    w_list, b_list = [], []

    f.write("###### TRAINING DATA ##########\n")

    for i in range(9):
        # update the slack
        svm1.update_c(math.pow(10, i))
        # fit the data
        svm1.fit(x_train, y_train)
        # get the weight and bias for the slack
        w, b = svm1.get_w_b()

        w_list.append(w)
        b_list.append(b)

        # use the weight and bias to predict on the training data
        y_pred = svm1.predict(x_train)
        print('i: ', i)
        print('c: ', math.pow(10, i))
        print('Confusion Matrix: \n', confusion_matrix(y_train, y_pred), '\n')
        print('Accuracy: ', accuracy_score(y_train, y_pred), '\n\n')

        # write to file for the result
        f.write("i: " + str(i) + "\n")
        f.write("c: " + str(math.pow(10, i)) + "\n")
        f.write("Confusion Matrix: \n" + str(confusion_matrix(y_train, y_pred)) + "\n")
        f.write("Accuracy: " + str(accuracy_score(y_train, y_pred)) + "\n\n")

    # data processing
    X_validate = spam_validate.drop('Y', axis=1)
    Y_validate = spam_validate['Y']
    Y_validate = [-1 if i == 0 else i for i in Y_validate]

    x_validate = np.asarray(X_validate)
    y_validate = np.asarray([np.float64(i) for i in Y_validate])

    best_acc = 0
    best_w = []
    best_b = []
    best_c = 0.0

    f.write("###### VALIDATION DATA ##########\n")
    # use the validation data to find the best weight and bias and slack
    for i in range(len(w_list)):
        # initialize the SVM with weight and bias
        svm1.initialize_w_b(w_list[i], b_list[i])
        # use the weight and bias to predict
        y_pred = svm1.predict(x_validate)

        # output the result
        print('i: ', i)
        print('c: ', math.pow(10, i))
        print('Confusion Matrix: \n', confusion_matrix(y_validate, y_pred), '\n')
        print('Accuracy: ', accuracy_score(y_validate, y_pred), '\n\n')
        # write to file for the result
        f.write("i: " + str(i) + "\n")
        f.write("c: " + str(math.pow(10, i)) + "\n")
        f.write("Confusion Matrix: \n" + str(confusion_matrix(y_validate, y_pred)) + "\n")
        f.write("Accuracy: " + str(accuracy_score(y_validate, y_pred)) + "\n\n")

        # store the best weight and bias
        if accuracy_score(y_validate, y_pred) > best_acc:
            best_acc = accuracy_score(y_validate, y_pred)
            best_w, best_b = w_list[i], b_list[i]
            best_c = math.pow(10, i)

    # data processing for the testing data
    X_test = spam_test.drop('Y', axis=1)
    Y_test = spam_test['Y']
    Y_test = [-1 if i == 0 else i for i in Y_test]

    x_test = np.asarray(X_test)
    y_test = np.asarray([np.float64(i) for i in Y_test])

    # initialize the svm with the best w and bias
    svm1.initialize_w_b(best_w, best_b)

    y_pred = svm1.predict(x_test)

    f.write("###### TESTING DATA ##########\n")

    # print the result on the testing data
    print("***Best w*** \n", best_w)
    print("Best b ", best_b)
    print("Best c ", best_c)

    print('Test Confusion Matrix: \n', confusion_matrix(y_test, y_pred), '\n')
    print('Test Accuracy: ', accuracy_score(y_test, y_pred), '\n')

    f.write("***Best w*** \n" + str(best_w) + "\n")
    f.write("Best b " + str(best_b) + "\n")
    f.write("Best c " + str(best_c) + "\n")

    f.write("Test Confusion Matrix: \n" + str(confusion_matrix(y_test, y_pred)) + "\n")
    f.write("Test Accuracy: " + str(accuracy_score(y_test, y_pred)) + "\n\n")

    f.close()


def main():
    linear_kernel_SVM()

if __name__ == '__main__':
    main()

