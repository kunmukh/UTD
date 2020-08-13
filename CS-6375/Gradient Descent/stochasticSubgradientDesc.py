# Kunal Mukherjee
# Stochastic Subgradient Learning
# 1/25/20

# import functions
import numpy as np
import csv

#import the data
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
w = np.zeros([4, 1], dtype=float)
b = 0

# vector to store the gradient descent
gradient_w = np.zeros([4, 1], dtype='float')
gradient_b = 0

step_size = 1
perceptron_loss = -1 # initialize value
classification = 0

num_iter = 0

m_data = points

FLAG_ALL_POINTS_CORR_CLASSF = True

# no points on the line
while True:

    # initialize value
    perceptron_loss = 0
    FLAG_ALL_POINTS_CORR_CLASSF = True

    for point in m_data:
        x = np.array(point[0], dtype=float)
        y = np.array(point[1], dtype=float)

        # predict the y according to the classifier
        predicted_y = np.sign(np.dot(w.T, x) + b)

        # predicted_y is correct or not
        classification = (-1 * y * predicted_y)

        # re-initialize the gradients
        gradient_w = 0
        gradient_b = 0

        # Wrong classification of data, so update the gradient of w and b
        if classification >= 0:
            gradient_w += -y * x.reshape(4, 1)
            gradient_b += -y
            FLAG_ALL_POINTS_CORR_CLASSF = False

        # Calculate perceptron loss
        perceptron_loss += max(0, (-1 * y * predicted_y))

        # Update w and b
        w = w - step_size * gradient_w
        b = b - step_size * gradient_b

        num_iter += 1

    print("\n\n(Iter)", num_iter, "perceptron_loss= ",
        perceptron_loss, "\nw=", w, "b=", b)

    if FLAG_ALL_POINTS_CORR_CLASSF:
        break

print("***\nFINAL", "(Iter)", num_iter, "\n w: ", w, "\nb: ", b,
      'perceptron_loss= ', perceptron_loss)