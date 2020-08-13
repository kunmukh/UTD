# Kunal Mukherjee
# 3/25/20
# HW 4
# CS 6363
# HW 4.2.1

# import statement
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def getSimilarityMatrix(data, sigma):
    # data is n x m matrix, n data points with m attributes
    # A  = n x n
    A = np.zeros(shape=(data.shape[0], data.shape[0]))

    for i in range(0, A.shape[0], 1):
        for j in range(i, A.shape[1], 1):
            A[i][j] = A[j][i] = np.exp((-1 / (2 * (sigma ** 2)))
                                       * np.power(np.linalg.norm(data.iloc[i] - data.iloc[j]), 2))

    return A


def getLaplacianMatrix(A):
    # creating a diagonal matrix
    D_Arr = []

    for i in range(A.shape[0]):
        sum_dig = 0
        for j in range(A.shape[1]):
            sum_dig += A[i][j]
        D_Arr.append(sum_dig)

    D = np.diag(D_Arr)

    return D - A

def getVMatrix(eig_val, eig_vec, k):

    # Make a list of (eigenvalue, eigenvector) tuples
    eig_pairs = [(np.abs(eig_val[i]), eig_vec[:, i]) for i in range(len(eig_val))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort(key=lambda x: x[0], reverse=False)

    # get the bottom k eigen vectors and value pair
    k_eig_pairs = eig_pairs[:k]

    V = np.hstack((k_eig_pairs[0][1].reshape(102, 1), k_eig_pairs[1][1].reshape(102, 1)))

    return V


def BasicAlgorithm(data, k, SIGMA):
    # get the similarity matrix
    A = getSimilarityMatrix(data, SIGMA)

    # print(A.shape,'Similarity Matrix:\n', pd.DataFrame(A))

    # Laplacian matrix
    L = getLaplacianMatrix(A)

    # print(L.shape, 'Laplacian Matrix:\n', pd.DataFrame(L))

    # eigenvectors of the Laplacian
    eig_val, eig_vec = np.linalg.eigh(L)

    print('Eigen value for L:', eig_val)

    # construct V matrix made of k small eigen vectors
    V = getVMatrix(eig_val, eig_vec, k)

    # print(V.shape, 'V Matrix:\n', pd.DataFrame(V))

    # cluster the rows of V into clusters S1,S2,...,Sk.
    kmeans = KMeans(n_clusters=k, random_state=0).fit(V)

    # get the labels for each eigen-vector
    label_y = kmeans.labels_

    # create the C1...Ck empty list
    C = [[] for _ in range(k)]

    # for all the eigenvector, ej, see which cluster, Si, it belongs to
    # get the corresponding data, dataj, and add it to the corresponding Ci cluster
    for count, lbl in enumerate(label_y):
        C[lbl].append(data.iloc[count])

    # Pb 4. 2.1 Complete

    return C


def plotCluster(C, plotTitle, center=None):

    fig = plt.figure()
    # for all cluster in C1

    for points in C[0]:
        plt.scatter(points[0], points[1], marker='.', facecolor='red')
    for points in C[1]:
        plt.scatter(points[0], points[1], marker='.', facecolor='blue')

    if center is not None:
        print(center)

        plt.scatter(center[0][0], center[0][1], marker='o', facecolor='red')
        plt.scatter(center[1][0], center[1][1], marker='o', facecolor='blue')

    plt.title(plotTitle)
    plt.savefig('img/BA/BA_' + plotTitle + '.png')


def kMeans(data, k):
    # cluster the data into clusters S1,S2,...,Sk.
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)

    # get the labels for each eigen-vector
    label_y = kmeans.labels_

    # create the C1...Ck empty list
    C = [[] for _ in range(k)]

    # for all the data, data_j, get the label, l, and add it to the corresponding labeled C_l cluster
    for count, lbl in enumerate(label_y):
        C[lbl].append(data.iloc[count])

    return C, kmeans.cluster_centers_


def main():
    # load the dataset
    data = pd.read_csv("../circs_m_return.data", sep='\t', header=None)

    K = 2
    SIGMA = [0.001, 0.01, 0.1, 1., 10., 1000., 10000., 100000., 1000000., 10000000.]

    for s in SIGMA:
        print(s)
        clusterC1 = BasicAlgorithm(data, K, s)

        plotCluster(clusterC1, "Simple Algorithm" + " SIGMA= " + str(s))

    clusterC2, clusterCenter = kMeans(data, K)

    plotCluster(clusterC2, "KMeans Algorithm", clusterCenter)

    # plot the combined cluster
    # plotCluster()

    plt.show()


if __name__ == '__main__':
    main()