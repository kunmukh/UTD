# Kunal Mukherjee
# Standard subgradient descent: Perceptron Learning
# 1/25/20
# import functions
import numpy as np
import csv

# import the data
datafile = open('perceptron.data', 'r')

myreader = csv.reader(datafile)

# a list to store the points
# structure [[x0,x1,x2,x3][y]]
points = []

# fill the points array
for row in myreader:
    x = []
    y = []
    point = []

    x.extend([row[0], row[1], row[2], row[3]])
    y.append(row[4])

    point.extend([x, y])
    points.append(point)

# create a weight vector and bias
w = np.zeros([4, 1], dtype='float')
b = 0

# vector to store the gradient descent
gradient_w = np.ones([4, 1], dtype='float')
gradient_b = 0

step_size = 1
perceptron_loss = -1 # initialize value
classification = 0

num_iter = 0

while np.linalg.norm(gradient_w) > 1e-5 or \
        np.linalg.norm(gradient_b) > 1e-5: # no points on the line

    # increase the num of iteration
    num_iter += 1

    # initialization of the values
    perceptron_loss = 0
    gradient_w = 0
    gradient_b = 0

    for point in points:
        x = np.array(point[0], dtype=float)
        y = np.array(point[1], dtype=float)

        # predict the y according to the classifier
        predicted_y = np.sign(np.dot(w.T, x) + b)

        classification = (-1 * y * predicted_y)
        print(classification)

        # Wrong classification of data, so update the gradient of w and b
        if classification >= 0:
            gradient_w += -y * x.reshape(4, 1)
            gradient_b += -y

        # calculate the perceptron loss
        perceptron_loss += max(0, (-1 * y * predicted_y))

    # Print the w,b, p_loss
    print("\n(Iter)", num_iter, "perceptron_loss= ", perceptron_loss, "\nw=\n", w, "\nb=", b)

    # Update w and b
    w = w - step_size * gradient_w
    b = b - step_size * gradient_b


print("***\nFINAL(Iter)", num_iter, "\nw:\n", w, "\nb: ", b,
      'perceptron_loss= ', perceptron_loss)