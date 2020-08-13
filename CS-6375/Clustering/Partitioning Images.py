# Kunal Mukherjee
# 3/25/20
# HW 4
# CS 6363
# HW 4.2.2

# import statement
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from PIL import Image


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

    V = np.hstack((k_eig_pairs[0][1].reshape(7500, 1)))

    return V


def SpectralClusteringAlgorithm(data, k, SIGMA):
    # get the similarity matrix
    A = getSimilarityMatrix(data, SIGMA)

    print(A.shape,'Similarity Matrix:\n', pd.DataFrame(A))

    # Laplacian matrix
    L = getLaplacianMatrix(A)

    print(L.shape, 'Laplacian Matrix:\n', pd.DataFrame(L))

    # eigenvectors of the Laplacian
    eig_val, eig_vec = np.linalg.eigh(L)

    # construct V matrix made of k small eigen vectors
    V = getVMatrix(eig_val, eig_vec, k)

    print(V.shape, 'V Matrix:\n', pd.DataFrame(V))

    # cluster the rows of V into clusters S1,S2,...,Sk.
    kmeans = KMeans(n_clusters=k, random_state=0).fit(V.reshape(-1, 1))

    # get the labels for each eigen-vector
    label_y = kmeans.labels_
    values_x = kmeans.cluster_centers_

    return label_y, values_x


def plotCluster(labels, values, plotTitle, img):

    # Create the segmented array from labels and values
    img_segm = np.choose(labels, values)
    # Reshape the array as the original image
    img_segm.shape = img.shape

    fig = plt.figure(1)

    # Plot the original image
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(img)
    ax1.set_title('Original image')

    # Plot the simplified color image
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.imshow(img_segm)
    ax2.set_title(plotTitle)

    # Get rid of the tick labels
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    plt.savefig('img/PI/PI_' + plotTitle + '.png')


def kMeans(data, k):
    # cluster the data into clusters S1,S2,...,Sk.
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)

    # get the labels and the cluster center
    label_y = kmeans.labels_
    values_x = kmeans.cluster_centers_

    return values_x, label_y


def getImageData(filename):
    image = Image.open(filename, 'r')

    # creating an array ofthe image
    A = np.array(image)

    print(pd.DataFrame(A.reshape((-1, 1))))

    return A, pd.DataFrame(A.reshape((-1, 1)))


def main():
    # load the dataset
    img, data = getImageData("../bw.jpg")

    K = 2
    SIGMA = [0.001, 0.01, 0.1, 1., 10., 1000.]

    # use the native k-means clustering
    values, labels = kMeans(data, K)
    plotCluster(labels, values, "KMeans Algorithm", img)

    # use the basic algorithm
    for s in SIGMA:
        print(s)
        labels, values = SpectralClusteringAlgorithm(data, K, s)
        plotCluster(labels, values, "Spectral Clustering" + " SIGMA= " + str(s), img)

    plt.show()


if __name__ == '__main__':
    main()