# Kunal Mukherjee
# 3/24/20
# HW 4
# CS 6363
# HW 4.1.1

# import statement
import numpy as np
import pandas as pd
from taSVM import SVMta

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


def SVM(train_x, train_y, test_x, test_y, c, featureSelection, k=None):

    s = SVMta()
    s.fit(train_x, train_y, c)
    acc = s.predict(test_x, test_y)

    if featureSelection:
        print("Accuracy with Feature Selection k: ", k, "c: ", c,
              "Test Accuracy SVM:", np.around(acc, 2), "Error SVM:", np.around(1 - acc, 2))
    else:
        print("Accuracy without Feature Selection c: ", c,
              "Test Accuracy SVM:", np.around(acc, 2), "Error SVM:", np.around(1 - acc, 2))


# main program
def main():
    # load the dataset
    train_x, train_y = get_x_y("../sonar_train.data", True)
    test_x, test_y = get_x_y("../sonar_test.data")
    validate_x, validate_y = get_x_y("../sonar_valid.data")

    # get the train matrix
    train_data_mat = train_x.T
    validate_data_mat = validate_x.T
    test_data_mat = test_x.T
    # print(train_data_mat)

    # covariance step
    train_data_mat_arr = np.asarray(train_data_mat)
    cov_data_train_x = [train_data_mat_arr[row, :] for row in range(train_data_mat_arr.shape[0])]

    # compute the covariance matrix
    cov_matrix = np.cov(cov_data_train_x)
    print(cov_matrix.shape, 'Cov Matrix:\n', cov_matrix)

    # eigenvectors and eigenvalues for the from the covariance matrix
    eig_val, eig_vec = np.linalg.eigh(cov_matrix)

    print(eig_val.shape, 'Eigen Value:\n', eig_val)
    print(eig_vec.shape, 'Eigen Vector:\n', eig_vec)

    for i in range(len(eig_val)):
        eigv = eig_vec[:, i].reshape(1, 60).T
        np.testing.assert_array_almost_equal(cov_matrix.dot(eigv), eig_val[i] * eigv,
                                             decimal=6, err_msg='', verbose=True)

    print("Test done!!!\n\n")

    # Make a list of (eigenvalue, eigenvector) tuples
    eig_pairs = [(np.abs(eig_val[i]), eig_vec[i]) for i in range(len(eig_val))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort(key=lambda x: x[0], reverse=True)

    # Print top 6 eigenvalue pair
    for i in range(6):
        print(eig_pairs[i][0])

    K = [[eig_pairs[0][1].reshape(60, 1)],
         [eig_pairs[0][1].reshape(60, 1), eig_pairs[1][1].reshape(60, 1)],
         [eig_pairs[0][1].reshape(60, 1), eig_pairs[1][1].reshape(60, 1), eig_pairs[2][1].reshape(60, 1)],
         [eig_pairs[0][1].reshape(60, 1), eig_pairs[1][1].reshape(60, 1), eig_pairs[2][1].reshape(60, 1),
          eig_pairs[3][1].reshape(60, 1)],
         [eig_pairs[0][1].reshape(60, 1), eig_pairs[1][1].reshape(60, 1), eig_pairs[2][1].reshape(60, 1),
          eig_pairs[3][1].reshape(60, 1), eig_pairs[4][1].reshape(60, 1)],
         [eig_pairs[0][1].reshape(60, 1), eig_pairs[1][1].reshape(60, 1), eig_pairs[2][1].reshape(60, 1),
          eig_pairs[3][1].reshape(60, 1), eig_pairs[4][1].reshape(60, 1), eig_pairs[5][1].reshape(60, 1)]]

    C = [1, 10, 100, 1000]

    best_k = 0
    best_c = 0
    best_error = 1

    for k_int, k in enumerate(K):
        # Choosing k=2 eigenvectors with largest eigenvalues
        matrix_w = np.hstack(k)
        # print('Matrix W:\n', matrix_w)

        # transforming to new samples
        transformed_train_data_x = matrix_w.T.dot(train_data_mat)
        # print('The new train data X:\n', pd.DataFrame(transformed_train_data_x))

        for c in C:

            svm1 = SVMta()
            svm1.fit(transformed_train_data_x.T, train_y, c)

            # transforming validate data to new samples
            transformed_validate_data_x = matrix_w.T.dot(validate_data_mat)
            # print('The new validate data X:\n', pd.DataFrame(transformed_validate_data_x))

            acc = svm1.predict(transformed_validate_data_x.T, validate_y)

            print("k: ", k_int+1, "c: ", c, "Validation Accuracy SVM:", np.around(acc, 2),
                  "Error SVM:", np.around(1-acc, 2))

            if 1-acc <= best_error:
                best_error = 1-acc
                best_c = c
                best_k = k_int
        print('\n')

    # print the best k and c pair based on validation data
    print("Best k: ", best_k, "Best c: ", best_c, "Best Validation Accuracy SVM:", np.around(1-best_error, 2),
          "Best Error SVM:", np.around(best_error, 2))

    matrix_w = np.hstack(K[best_k])
    # print('Matrix W:\n', matrix_w)

    # transforming data to new data
    transformed_train_data_x = matrix_w.T.dot(train_data_mat)
    # print('The new train data X:\n', pd.DataFrame(transformed_train_data_x))

    transformed_test_data_x = matrix_w.T.dot(test_data_mat)
    # print('The new test data X:\n', pd.DataFrame(transformed_test_data_x))

    # ACCURACY WITH Feature Selection
    SVM(transformed_train_data_x.T, train_y, transformed_test_data_x.T, test_y, best_c, True, best_k)

    # ACCURACY WITHOUT Feature Selection
    SVM(np.asarray(train_x), np.asarray(train_y), np.asarray(test_x), np.asarray(test_y), best_c, False)


if __name__ == '__main__':
    main()