# Kunal Mukherjee
# 5/1/20
# HW 6
# CS 6375
# PB 2.2.1

# import statements
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import multivariate_normal as mvn
import random
from sklearn.metrics import confusion_matrix
from statistics import mode

# get the data
def get_x(filename):

    # load the dataset
    data = pd.read_csv(filename, header=None)

    # print the data
    # print('Data:\n', data)

    # remove the last label column
    data_x = data.drop(data.columns[0], axis=1)
    data_y = np.asarray(data.iloc[:, 0])

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

    return data_x_norm_variance, data_y


class GMM:

    def __init__(self, k, n_runs):
        self.C = k  # number of Guassians/clusters
        self.n_runs = n_runs

    def get_params(self):
        return self.mu, self.pi, self.sigma

    def _initialise_parameters(self, X):

        d = X.shape[1]
        self.shape = X.shape
        self.n, self.m = self.shape

        self._initial_means = np.zeros((self.C, d))
        self._initial_cov = np.zeros((self.C, d, d))
        self._initial_pi = np.zeros(self.C)

        for m in range(len(self._initial_means)):
            self._initial_means[m] = X[np.random.randint(low=0, high=self.n), :]

        idt = np.identity((X.shape[1]))
        id_lst = [idt for _ in range(self.C)]
        self._initial_cov = np.asarray(id_lst)

        self._initial_pi = np.full(shape=self.C, fill_value=1/self.C)

        return self._initial_means, self._initial_cov, self._initial_pi

    def _e_step(self, X, pi, mu, sigma):
        N = X.shape[0]
        self.gamma = np.zeros((N, self.C))

        const_c = np.zeros(self.C)

        self.mu = self.mu if self._initial_means is None else self._initial_means
        self.pi = self.pi if self._initial_pi is None else self._initial_pi
        self.sigma = self.sigma if self._initial_cov is None else self._initial_cov
        if self.C < 24:
            self.reg_cov = 1e-6 * np.identity(len(X[0]))
        else:
            self.reg_cov = 1e-4 * np.identity(len(X[0]))

        for c in range(self.C):
            # Posterior Distribution using Bayes Rule
            self.sigma[c] += self.reg_cov
            self.gamma[:, c] = self.pi[c] * mvn.pdf(X, self.mu[c, :], self.sigma[c])

        # normalize across columns to make a valid probability
        gamma_norm = np.sum(self.gamma, axis=1)[:, np.newaxis]
        self.gamma /= gamma_norm

        return self.gamma

    def _m_step(self, X, gamma):
        C = self.gamma.shape[1]  # number of clusters
        # responsibilities for each gaussian
        self.pi = np.mean(self.gamma, axis=0)
        self.mu = np.dot(self.gamma.T, X) / np.sum(self.gamma, axis=0)[:, np.newaxis]

        for c in range(C):
            x = X - self.mu[c, :]  # (N x d)

            gamma_diag = np.diag(self.gamma[:, c])
            x_mu = np.matrix(x)
            gamma_diag = np.matrix(gamma_diag)

            sigma_c = x.T * gamma_diag * x
            self.sigma[c, :, :] = (sigma_c) / np.sum(self.gamma, axis=0)[:, np.newaxis][c]

        return self.pi, self.mu, self.sigma

    def _compute_loss_function(self, X, pi, mu, sigma):
        N = X.shape[0]
        C = self.gamma.shape[1]
        self.loss = np.zeros((N, C))

        for c in range(C):
            dist = mvn(self.mu[c], self.sigma[c], allow_singular=True)
            self.loss[:, c] = self.gamma[:, c] * (
                        np.log(self.pi[c] + 0.00001) + dist.logpdf(X) - np.log(self.gamma[:, c] + 0.000001))
        self.loss = np.sum(self.loss)
        return self.loss

    def fit(self, X):

        self.mu, self.sigma, self.pi = self._initialise_parameters(X)

        for run in range(self.n_runs):
            self.gamma = self._e_step(X, self.mu, self.pi, self.sigma)
            self.pi, self.mu, self.sigma = self._m_step(X, self.gamma)
            loss = self._compute_loss_function(X, self.pi, self.mu, self.sigma)

            # print("Iteration: %d Loss: %0.6f" % (run, loss))

    def predict(self, X):
        labels = np.zeros((X.shape[0], self.C))
        if self.C <= 24:

            self.reg_cov = 1e-6 * np.identity(len(X[0]))
        else:
            self.reg_cov = 1e-4 * np.identity(len(X[0]))

        for c in range(self.C):
            self.sigma[c] += self.reg_cov
            labels[:, c] = self.pi[c] * mvn.pdf(X, self.mu[c, :], self.sigma[c])
        labels = labels.argmax(1)
        return labels

    def predict_proba(self, X):
        post_proba = np.zeros((X.shape[0], self.C))

        for c in range(self.C):
            # Posterior Distribution using Bayes Rule
            post_proba[:, c] = self.pi[c] * mvn.pdf(X, self.mu[c, :], self.sigma[c])

        return post_proba


def main():
    k = [12, 18, 24, 36, 42]
    x, y = get_x("../leaf.data")
    print(x)

    x = x.values

    for ki in k:
        losses = []
        for _ in range(20):
            model = GMM(ki, n_runs=30)
            model.fit(x)
            # print(model.loss)
            losses.append(model.loss)

        print('k: ', ki, 'mean: ', np.mean(losses), 'var: ', np.var(losses))

    # test with true values
    model = GMM(36, n_runs=30)
    model.fit(x)
    print(model.predict(x))


if __name__ == '__main__':
    main()
