# Kunal Mukherjee
# 3/24/20
# HW 4
# CS 6363
# HW 4.1.2

# import statement
import numpy as np
import pandas as pd
from taSVM import SVMta
import csv

# global constants
train_mean = None
train_variance = None


def get_x_y(filename, isTrain=False):
    global train_mean, train_variance

    # load the dataset
    data = pd.read_csv(filename, header=None)

    # print the data
    # print('Data:\n', data)

    # remove the last label column
    data_x = data.drop(data.columns[60], axis=1)
    data_y = np.asarray(data.iloc[:, -1])
    data_y[data_y > 1] = -1

    if isTrain:
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


    else:
        # center the attribute or normalize the mean
        data_x_centered = data_x - train_mean
        # print('Data X Centered:\n', data_x_centered)

        # normalize the variance
        data_x_norm_variance = data_x_centered / train_variance
        # print('Data X Norm Var:\n', data_x_norm_variance)

    return data_x_norm_variance, data_y


def getAvgError100experiements(train_data_matrix, train_y,
                               validate_data_matrix, validate_y,
                               test_data_matrix, test_y):
    train_x = train_data_matrix.T
    test_x = test_data_matrix.T
    validate_x = validate_data_matrix.T

    C = [1, 10, 100, 1000]

    error_list = []
    accur_list = []

    # initialize the best_c and acc
    best_c = 0
    best_err = 1

    # for all the c
    for c in C:
        error = 0

        # declare a support vector machine with c
        svm1 = SVMta()
        svm1.fit(np.asarray(train_x), np.asarray(train_y), c)

        # run 100 experiments
        for i in range(100):

            # find the accuracy of the predictions
            acc = svm1.predict(np.asarray(validate_x), np.asarray(validate_y))
            error += (1. - acc)
        # get the average error and acc
        avg_acc = 1-error/100.
        avg_err = error/100.

        if avg_err <= best_err:
            best_err = avg_acc
            best_c = c

    # declare a SVM with best slack c
    svm2 = SVMta()
    svm2.fit(np.asarray(train_x), np.asarray(train_y), best_c)

    # find the accuracy of the predictions
    acc = svm2.predict(np.asarray(test_x), np.asarray(test_y))
    error = (1. - acc)

    # return the error and accuracy
    return error, acc


def main():
    K = [i for i in range(1, 11)]
    S = [i for i in range(1, 21)]

    train_x, train_y = get_x_y("../sonar_train.data", True)
    test_x, test_y = get_x_y("../sonar_test.data")
    validate_x, validate_y = get_x_y("../sonar_valid.data")

    print(train_x, train_y)

    # the columns of the data matrix are the input
    # data points
    train_data_matrix = train_x.T
    print('train data mat:\n', train_data_matrix)
    test_data_matrix = test_x.T
    validate_data_matrix = validate_x.T


    # Compute the top k eigenvalues and
    # eigenvectors of the covariance matrix corresponding to
    # the data matrix

    # covariance matrix
    # covariance step
    train_data_mat_arr = np.asarray(train_data_matrix)
    cov_data_train_x = [train_data_mat_arr[row, :] for row in range(train_data_mat_arr.shape[0])]

    # compute the covariance matrix
    cov_matrix = np.cov(cov_data_train_x)
    print(cov_matrix.shape, 'Cov Matrix:\n', cov_matrix)

    # eigenvectors and eigenvalues for the from the covariance matrix
    eig_val_cov, eig_vec_cov = np.linalg.eigh(cov_matrix)

    print(eig_vec_cov.shape, 'Eig Vec:\n', eig_vec_cov)

    for i in range(len(eig_val_cov)):
        eigv = eig_vec_cov[:, i].reshape(1, 60).T
        np.testing.assert_array_almost_equal(cov_matrix.dot(eigv), eig_val_cov[i] * eigv,
                                             decimal=6, err_msg='', verbose=True)

    print("Test Done!!!")

    # Make a list of (eigenvalue, eigenvector) tuples
    eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:, i]) for i in range(len(eig_val_cov))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort(key=lambda x: x[0], reverse=True)

    # a csv file to store the data
    f = open("FeatSelecData.csv", "w+", newline='')
    fieldnames = ['k', 's', 'Accuracy', 'Error']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()


    for k in K:
        # get the top k eigen vectors and value pair
        k_eig_pairs = eig_pairs[:k]

        # π is a vector. π_j as the probability of sampling column j
        PI = []

        for j in range(train_data_matrix.shape[0]):
            sum_eig_vec = 0
            for i in range(k):
                sum_eig_vec += k_eig_pairs[i][1][j] ** 2
            PI.append(sum_eig_vec/k)

        PI = np.asarray(PI)

        # print('PI size: ', PI.shape, 'PI: \n', PI, 'PI sum: ', np.sum(PI))

        # normalize the PI
        PI /= PI.sum()

        # generate s columns independently at random from the distribution π
        for s in S:
            row_num = set()
            # get s columns independently
            for _ in range(s):
                row_num.add(np.random.choice(np.arange(0, 60), p=PI.astype('float64')))

            # change col_num to list
            row_num = list(row_num)

            # select the training data
            selected_train_data_matrix = train_data_matrix.loc[row_num, :]

            # print('selected train data mat:\n', selected_train_data_matrix)

            # select the testing and validation data
            selected_test_data_matrix = test_data_matrix.loc[row_num, :]
            selected_validate_data_matrix = validate_data_matrix.loc[row_num, :]

            # print('selected train data mat:\n', selected_test_data_matrix)

            # get the average test error for 100 experiments
            avg_error, avg_accur = getAvgError100experiements(selected_train_data_matrix, train_y,
                                                              selected_validate_data_matrix, validate_y,
                                                              selected_test_data_matrix, test_y)

            print('k: ', k, 's: ', s, 'Avg Accur', avg_accur, 'Avg Error', avg_error)
            writer.writerow({'k': k, 's': s, 'Accuracy': np.around(avg_accur, 3), 'Error': np.around(avg_error, 3)})


if __name__ == '__main__':
    main()