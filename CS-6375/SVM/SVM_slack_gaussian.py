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
SIGMA_SQ = 1.


# the linear kernel
def gaussian_kernel(x, y, sigma_sq=SIGMA_SQ):
    return np.exp(-np.linalg.norm(x-y)**2 / (2 * sigma_sq))


class SVM:
    def __init__(self, c=0, kernel=gaussian_kernel):
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

        # print the c and sigma
        print(self.c)
        print(SIGMA_SQ)

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
        cvxopt.solvers.options['abstol'] = 1e-8
        cvxopt.solvers.options['reltol'] = 1e-7

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

        # Intercept
        self.b = 0
        for i in range(len(X)):
            inner_sum = 0
            for j in range(len(self.non_0_lagrange_multiplier)):
                inner_sum -= self.non_0_lagrange_multiplier[j] * \
                          self.support_vector_classfication[j] * \
                          self.kernel(self.support_vector[j], X[i])
            self.b += (1 / y[i]) - inner_sum
        self.b /= len(non_0_lagrange_multiplier_indices)

    def predict(self, X):
        y_pred = []

        # itearte over the sample x
        for x in X:
            prediction = 0
            # predict the label of the sample
            for i in range(len(self.non_0_lagrange_multiplier)):
                prediction += self.non_0_lagrange_multiplier[i] *\
                              self.support_vector_classfication[i] *\
                              self.kernel(self.support_vector[i], x)
            prediction += self.b
            y_pred.append(np.sign(prediction))

        return np.array(y_pred)

    def initialize_w_b(self, w, b):
        self.w = w
        self.b = b

    def update_c(self, c):
        self.c = float(c)

    def get_w_b(self):
        return self.w, self.b


def gaussian_kernel_SVM():
    # Open the file for writing output
    f = open("outputGaussSVM.txt", "w")

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

    # data processing
    X_validate = spam_validate.drop('Y', axis=1)
    Y_validate = spam_validate['Y']
    Y_validate = [-1 if i == 0 else i for i in Y_validate]

    x_validate = np.asarray(X_validate)
    y_validate = np.asarray([np.float64(i) for i in Y_validate])

    # initialize an svm
    svm1 = SVM()

    # create a weight and bias list
    w_list = np.zeros((9, 5), dtype=object)
    b_list = np.zeros((9, 5), dtype=object)

    # get the best w, b, c
    best_acc = 0
    best_w = []
    best_b = []
    best_c = 0.0
    best_SIGMA = 0.0

    global SIGMA_SQ

    for i in range(0, 9):
        for j in range(-1, 4):

            SIGMA_SQ = pow(10, j)
            svm1.update_c(math.pow(10, i))

            svm1.fit(x_train, y_train)
            w, b = svm1.get_w_b()

            w_list[i, j] = w
            b_list[i, j] = b
            # lagrange_list[i, j], sv_list[i, j], sv_y_list[i, j] = svm1.get_lagranage_sv_sv_y()

            y_pred = svm1.predict(x_train)

            print("###### TRAINING DATA ##########\n")
            print('i: ', i)
            print('j: ', j)
            print('c: ', math.pow(10, i))
            print('sigma^2: ', math.pow(10, j))
            print('Confusion Matrix: \n', confusion_matrix(y_train, y_pred), '\n')
            print('Accuracy: ', accuracy_score(y_train, y_pred), '\n\n')

            f.write("###### TRAINING DATA ##########\n")
            f.write("i: " + str(i) + "\n")
            f.write("j: " + str(j) + "\n")
            f.write("c: " + str(math.pow(10, i)) + "\n")
            f.write("sigma^2: " + str(math.pow(10, j)) + "\n")
            f.write("Confusion Matrix: \n" + str(confusion_matrix(y_train, y_pred)) + "\n")
            f.write("Accuracy: " + str(accuracy_score(y_train, y_pred)) + "\n\n")

            y_pred = svm1.predict(x_validate)

            print("###### VALIDATION DATA ##########\n")
            print('i: ', i)
            print('j: ', j)
            print('c: ', math.pow(10, i))
            print('sigma^2: ', math.pow(10, j))
            print('Confusion Matrix: \n', confusion_matrix(y_validate, y_pred), '\n')
            print('Accuracy: ', accuracy_score(y_validate, y_pred), '\n\n')

            f.write("###### VALIDATION DATA ##########\n")
            f.write("i: " + str(i) + "\n")
            f.write("j: " + str(j) + "\n")
            f.write("c: " + str(math.pow(10, i)) + "\n")
            f.write("sigma^2: " + str(math.pow(10, j)) + "\n")
            f.write("Confusion Matrix: \n" + str(confusion_matrix(y_validate, y_pred)) + "\n")
            f.write("Accuracy: " + str(accuracy_score(y_validate, y_pred)) + "\n\n")

            if accuracy_score(y_validate, y_pred) > best_acc:
                best_acc = accuracy_score(y_validate, y_pred)
                best_w, best_b = svm1.get_w_b()
                # best_lagrange, best_sv, best_sv_y = lagrange_list[i][j], sv_list[i][j], sv_y_list[i][j]
                best_c = math.pow(10, i)
                best_SIGMA = math.pow(10, j)


    # data processing for the testing data
    X_test = spam_test.drop('Y', axis=1)
    Y_test = spam_test['Y']
    Y_test = [-1 if i == 0 else i for i in Y_test]

    x_test = np.asarray(X_test)
    y_test = np.asarray([np.float64(i) for i in Y_test])

    # initialize the svm with the best w and bias
    svm2 = SVM()
    SIGMA_SQ = best_SIGMA
    svm2.update_c(best_c)

    svm2.fit(x_train, y_train)

    y_pred = svm2.predict(x_test)

    f.write("###### TESTING DATA ##########\n")

    # print the result on the testing data
    print("***Best w*** \n", best_w)
    print("Best b ", best_b)
    print("Best c ", best_c)
    print("Best SIGMA^2 ", best_SIGMA)
    print('Test Confusion Matrix: \n', confusion_matrix(y_test, y_pred), '\n')
    print('Test Accuracy: ', accuracy_score(y_test, y_pred), '\n')

    f.write("***Best w*** \n" + str(best_w) + "\n")
    f.write("Best b " + str(best_b) + "\n")
    f.write("Best c " + str(best_c) + "\n")
    f.write("Best SIGMA^2 " + str(best_SIGMA) + "\n")
    f.write("Test Confusion Matrix: \n" + str(confusion_matrix(y_test, y_pred)) + "\n")
    f.write("Test Accuracy: " + str(accuracy_score(y_test, y_pred)) + "\n\n")

    f.close()


def main():
    gaussian_kernel_SVM()


if __name__ == '__main__':
    main()