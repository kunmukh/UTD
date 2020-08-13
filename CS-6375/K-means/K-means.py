# Kunal Mukherjee
# 5/1/20
# HW 6
# CS 6375
# PB 2.1.1

# import statements
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import KMeans

# get the data
def get_x(filename):

    # load the dataset
    data = pd.read_csv(filename, header=None)

    # print the data
    # print('Data:\n', data)

    # remove the last label column
    data_x = data.drop(data.columns[0], axis=1)

    # compute the mean
    train_mean = data_x.mean(axis=0)
    # print('Data X Mean:\n', data_x_mean)

    # center the attribute or normalize the mean
    data_x_centered = data_x - train_mean
    # print('Data X Centered:\n', data_x_centered)

    # compute the variance
    train_variance = data_x_centered.std(axis=0)
    # print('Data X Var:\n', train_variance)

    # normalize the variance
    data_x_norm_variance = data_x_centered / train_variance
    # print('Data X Norm Var:\n', data_x_norm_variance)

    return data_x_norm_variance


# K-means class
class K_Means:

    def __init__(self, k =3, tolerance = 0.0001, max_iterations = 10000):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def fit(self, data):

        self.centroids = {}

        # initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        for i in range(self.k):
            temp = data[i]
            for j in range(len(temp)):
                temp[j] = np.random.uniform(-3, 3)

            self.centroids[i] = temp

        # begin iterations
        for i in range(self.max_iterations):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            # find the distance between the point and cluster; choose the nearest centroid
            for features in data:
                distances = [np.linalg.norm(features - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classes[classification].append(features)

            previous = dict(self.centroids)

            # average the cluster data points to re-calculate the centroids
            for classification in self.classes:
                self.centroids[classification] = np.average(self.classes[classification], axis=0)

            isOptimal = True

            for centroid in self.centroids:

                original_centroid = previous[centroid]
                curr = self.centroids[centroid]

                if np.sum((curr - original_centroid) / original_centroid * 100.0) > self.tolerance:
                    isOptimal = False

            # break out of the main loop if the results are optimal,
            # ie. the centroids don't change their positions much(more than our tolerance)
            if isOptimal:
                # calculate the mean and variance of the objective
                self.loss = 0
                for count, c in enumerate(self.centroids):
                    for cl in self.classes[count]:
                        self.loss += np.linalg.norm(cl - c)

                break

    def pred(self, data):
        distances = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification


def main():
    k = [12, 18, 24, 36, 42]
    x = get_x("../leaf.data")
    print(x)

    x = x.values

    for ki in k:
        # km = K_Means(ki)
        losses = []

        for _ in range(20):
            # km.fit(x)
            km = KMeans(n_clusters=ki, init='random').fit(x)

            losses.append(km.inertia_)

        print('k: ', ki, 'mean: ', np.mean(losses), 'var: ', np.var(losses))

    # test with true values
    model = K_Means(36)
    model.fit(x)
    pred = [model.pred(xi) for xi in x]
    print(pred)


if __name__ == '__main__':
    main()