# Kunal Mukherjee
# 4/21/20
# HW 5 P3.1 Naive Bayes
# CS 6375

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from csv import reader

# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


# Convert string column to integer
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup


# get the X and Y separately
def getXY(dataset):

    X = []
    Y = []

    for row in dataset:
        X.append(row[0: -1])
        Y.append(row[-1])

    return np.asarray(X), np.asarray(Y)


# the data from teh file
def getDate(filename):
    dataset = load_csv(filename)
    for i in range(len(dataset[0]) - 1):
        str_column_to_float(dataset, i)
    # convert class column to integers
    str_column_to_int(dataset, len(dataset[0]) - 1)

    X, y = getXY(dataset)
    y = y[:, np.newaxis]

    return X, y

# the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Loss function for logistic regression
def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(np.matmul(X, theta))
    cost = (-1/m)*((np.matmul(y.T, np.log(h)))+(np.matmul((1-y).T, np.log(1-h))))
    return cost


# gradient descent rule
def gradient_descent(X, y, theta, learning_rate, iterations):
    m = len(y)
    cost_history = np.zeros((iterations, 1))
    # learning_rate = 1

    for i in range(iterations):
        h_x = sigmoid(np.matmul(X, theta))
        theta = theta - learning_rate * ((1/m) * np.matmul(X.T, h_x - y))
        cost_history[i] = compute_cost(X, y, theta)
        # learning_rate = 2 / (2+i)

    return cost_history, theta


# prediction
def predict(X, theta):
    return np.round(sigmoid(np.matmul(X, theta)))


def main():
    X, y = getDate('../data/sonar_train.data')
    X = np.hstack((np.ones((len(y), 1)), X))

    theta = np.zeros((np.size(X, 1), 1))
    iterations = 100000
    learning_rate = 0.1

    initial_cost = compute_cost(X, y, theta)
    print("Initial Cost is: {} \n".format(initial_cost))

    (cost_history, theta_optimal) = gradient_descent(X, y, theta, learning_rate, iterations)
    print("Final Cost is: {} \n".format(cost_history[-1]))

    print("Optimal Parameters are: \n", theta_optimal, "\n")

    # get the testing data
    X, y = getDate('../data/sonar_test.data')
    X = np.hstack((np.ones((len(y), 1)), X))

    # prediction step
    y_pred = predict(X, theta_optimal)
    # get the accuracy score
    score = float(sum(y_pred == y)) / float(len(y))

    # print the accuracy score
    print("Accuracy:", score)

    # print the loss function
    plt.figure()
    sns.set_style('white')
    plt.plot(range(len(cost_history)), cost_history, 'r')
    plt.annotate(str(cost_history[0]), (0, cost_history[0]))
    plt.annotate(str(cost_history[-1]), (len(cost_history), cost_history[-1]))
    plt.title("LogReg Convergence Graph of Cost Function| Accuracy: " + str(np.round(score, 2)))
    plt.xlabel("Number of Iterations")
    plt.ylabel("Cost")

    plt.show()


if __name__ == '__main__':
    main()