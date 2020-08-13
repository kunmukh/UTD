import pandas as pd
import numpy as np
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import cvxopt
import math

# mystery_data = pd.read_csv("perceptron.data")
mystery_data = pd.read_csv("mystery.data")

# print(mystery_data.shape)
# print(mystery_data.head())

X = mystery_data.drop('Y', axis=1)
Y = mystery_data['Y']

X = np.asarray(X)
Y = np.asarray([np.float64(i) for i in Y])

# print(X.head())
# print(Y.head())

class SVM:
    def __init__(self):
        self.w = np.zeros(1)
        self.b = 0

    def fit(self, X, y, OrgX):
        n_samples, n_features = X.shape

        # P = x^Tx
        # X = [[x11y1 x21y2 ... Xn1Yn] feature(d) x samples(n)
        #      [x12y2 x22y2 ... Xn1Yn]
        #      [x13y2 x23y2 ... Xn1Yn]
        #               :
        #      [x1dy2 x2dy2 ... XndYn]
        x = np.asarray([X[i]*y[i] for i in range(n_samples)]).T # 12 x 800

        P = cvxopt.matrix(np.dot(x.T, x))

        # q = -1 (1 x N)
        q = cvxopt.matrix(np.ones(n_samples) * -1)

        # A = y^T
        A = cvxopt.matrix(y, (1, n_samples))

        # b = 0
        b = cvxopt.matrix(0.0)

        # G = -1 (N x N)
        G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))

        # h = 0 (1 x N)
        h = cvxopt.matrix(np.zeros(n_samples))

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
        non_0_lagrange_multiplier = lagrange_multipler[non_0_lagragnge_boolean_arr]
        # print('non_0_lagrange_multiplier: \n', non_0_lagrange_multiplier)

        # support vectors are the vectors that have the lagrange multiplier
        support_vector = X[non_0_lagragnge_boolean_arr]
        # for i in non_0_lagrange_multiplier_indices:
        #    print('Original Support Vec', OrgX[i])

        # support vector's classification
        support_vector_classfication = y[non_0_lagragnge_boolean_arr]
        # print('support_vector_classfication: \n', support_vector_classfication)

        # Weights
        self.w = np.zeros(n_features)
        for n in range(len(non_0_lagrange_multiplier)):
            self.w += non_0_lagrange_multiplier[n] * support_vector_classfication[n] * support_vector[n]
        print('Optimal Margin', np.linalg.norm(self.w))

        # Intercept
        self.b = 0
        for i in non_0_lagrange_multiplier_indices:
            self.b += (1/y[i]) - np.dot(self.w.T, X[i])
        self.b /= len(non_0_lagrange_multiplier_indices)

    def initialize_w_b(self, w, b):
        self.w = w
        self.b = b

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def predict(self, X):
        return np.sign(self.project(X))

'''Optimal solution found.
intercept:  -2362.8563613008996
weight:  [ 3505.82258006   -25.36619549  -110.80333688  -704.60962567
  2811.51572215   -34.2337497    273.08625763 -3475.911107
  5103.67752073   163.51390858 -1678.11707386   865.37476353]
Confusion Matrix: 
 [[ 30   0]
 [  2 168]]
Accuracy:  0.99'''

def feature_transform(x):
    return np.asarray([[x[0], x[1], x[2], x[3],
                        math.exp(x[0]*x[1]),
                        math.exp(x[2]*x[3]),
                        math.exp(x[0]*x[2])*math.sin(x[2]),
                        math.exp(x[1]*x[3])*math.sin(x[0]),
                        math.pow(x[0]*x[1], 2)*x[2],
                        math.pow(x[1]*x[2], 2)*x[3],
                        x[0]*x[1]*x[2]*math.exp(x[0]*math.sin(x[1]*x[2])),
                        x[0]*x[1]*x[2]*math.exp(x[1]*math.sin(x[2]*x[3]))] for x in X])


X_feature = feature_transform(X)

x_train, x_test, y_train, y_test = train_test_split(X_feature, Y, test_size = 0.20)


svm1 = SVM()
svm1.fit(x_train, y_train, X)

# used for checking
# svm.initialize_w_b( [   2.23847990e+03, -7.41714319e-01, -8.31086076e+01, -3.25429235e+02,
#                         1.79675994e+03,  6.11340816e+00,  1.37895332e+02, -2.25604044e+03,
#                         3.29338113e+03,  5.84349622e+01, -1.23295591e+03,  7.21755801e+02],-1612.8261217324493)

print('intercept: ', svm1.b)
print('weight: ', svm1.w)

y_pred = svm1.predict(x_test)

print('Confusion Matrix: \n', confusion_matrix(y_test, y_pred))
print('Accuracy: ', accuracy_score(y_test, y_pred))


'''x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.20)

svmClassifier = svm.SVC(kernel='linear')
svmClassifier.fit(x_train, y_train)

y_predict = svmClassifier.predict(x_test)

print('\nConfusion Matrix:\n',confusion_matrix(y_test, y_predict))
# print(classification_report(y_test,y_predict))

# find the accuracy of the predictions
acc = metrics.accuracy_score(y_test, y_predict)

print("Accuracy SVM:", acc)

# for count, i in enumerate(svmClassifier.support_vectors_):
#     print('i: ', count, 'support_vector', i, "|| w ||:", np.linalg.norm(i))

# print('# of supp vec:', svmClassifier.n_support_)
print('Coff: ' , svmClassifier.coef_, "|| w ||:", np.linalg.norm(svmClassifier.coef_))
print('Incpt: ', svmClassifier.intercept_)'''

