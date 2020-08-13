# Kunal Mukherjee
# 3/7/2020
# CS 6375
# Homework 3

# import the libraries
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import math
import pickle
import itertools
import copy


# get the header and the data
def getData(filename):

    data = pd.read_csv(filename)

    # header manipulation
    cols = data.columns.tolist()
    cols = cols[1:23] + cols[0:1]

    data = data[cols]

    # change the Y value 0 to -1
    data.loc[data['Y'] == 0, 'Y'] = -1

    # data manipulation based on the header
    return data, cols


# return the unique values for a column in a data
def unique_vals(data, colName):
    return data[colName].value_counts().keys().tolist()


# return the unique samples and their occurrence count in the dataset
def label_counts(data):
    values = data["Y"].value_counts().tolist()
    keys = data["Y"].value_counts().keys().tolist()
    return dict(zip(keys, values))


# test usage [q = Question(header.index("X0"), '0', header)]
class Question:
    # the Question is used to partition a dataset.

    def __init__(self, column, value, header):
        self.column = column
        self.value = value
        self.valString = header[column]

    # The 'match' method is used to check
    # the feature value in an given row
    # with the feature value stored in the question.
    # question.match(row)
    def match(self, row, header):
        # Compare the feature value in an example to the
        # feature value in this question.
        col = header.index(self.valString)
        val = row[col]

        return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="

        return "Is %s %s %s?" % (
            self.valString, condition, str(self.value))


# Partition the dataset based on if a particular feature
# has an expected value or not
# [true_rows, false_rows = partition(mush_train, Question(0, "f"))]
def partition(data, question, header):

    # for each row in the dataset
    # check if the row matches the expected value of a given question
    true_rows, false_rows = [], []
    for row in data.values:
        if question.match(row, header):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


class Leaf:
    # leaf node holds the label for the data that is left
    def __init__(self, data):

        '''values = data["Y"].value_counts().tolist()
                    keys = data["Y"].value_counts().keys().tolist()

                    max_val_ind = np.argmax(values)
                    key = keys[max_val_ind]

                    self.predictions = dict(zip(keys, values))
                    self.maxprediction = dict({key: values[max_val_ind]})'''

        self.predictions = dict({data: 100})
        self.maxprediction = dict({data: 100})


class Decision_Node:
    # Decision node contains a question
    # It contains the data set that answered true
    # It contains the data set that answered false
    # It contains the IG for that node
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


# Find all the question for a given column
# Usage [find_all_question(data_train, 'X0', header)]
def find_all_question(data, attrName, header):
    questions = []
    vals = unique_vals(data, attrName)

    for val in vals:
        questions.append(Question(header.index(attrName), val, header))

    return questions

# build the forest for an attribute
def build_tree(data, depth):
    # header
    header = data.columns.tolist()

    all_questions = []

    # Find all the question possible for the given attribute
    for h in header[:-1]:
        all_questions.append(find_all_question(data, h, header))

    decision_nodes = []

    all_label = list(itertools.product([-1, 1], repeat=2))

    # create a decision tree for every attribute
    for questions1 in all_questions:

        # making tree 1-4
        # the true decision node for second question 0
        for lbl in all_label:
            true_leaf = Leaf(lbl[0])

            # the false leaf
            false_leaf = Leaf(lbl[1])

            decision_nodes.append(Decision_Node(questions1[0], true_leaf, false_leaf))

        ''''# the true decision node for second question 0
        for lbl in all_label:
            true_leaf = Leaf(lbl[0])

            # the false leaf
            false_leaf = Leaf(lbl[1])

            decision_nodes.append(Decision_Node(questions1[1], true_leaf, false_leaf))'''

    # Return all the possible of one split for the particular attribute
    return decision_nodes


# prints the tree
# [print_tree(my_tree)]
def print_tree(node, spacing=""):

    # Base case: the node is a leaf
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.maxprediction)
        return

    # Print the question at this node
    # It is a decision node
    # print the question and the gain
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    # Call this function recursively on the true branch
    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


# print the forest
def print_tree1d(nodes, spacing=""):

    for node in nodes:
        # Base case: we've reached a leaf
        if isinstance(node, Leaf):
            print(spacing + "Predict", node.maxprediction)
            return

        # Print the question at this node
        print(spacing + str(node.question))

        # Call this function recursively on the true branch
        # print(spacing + '--> True:')
        print_tree(node.true_branch, spacing + 'True  --> :' + "  ")

        print_tree(node.false_branch, spacing + 'False --> :' + "  ")


# return the header
def getHeader():
    return ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
            'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'Y']

# Classifies the row based on the tree's root node given
# [classify(mush_train.values[2], my_tree)]
def classify(row, node):
    # load the header
    header = getHeader()

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return list(node.maxprediction)[0]

    # Decide whether to follow the true-branch or the false-branch
    # Use the question(feature / value) the node
    # to select which branch to follow
    if node.question.match(row, header):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


# classify the row, based on all the question for a given feature
def classify1d(row, nodes, header):
    # get the classification for an row
    # using a list of nodes
    classifications = []

    if isinstance(nodes, Leaf):
        return nodes.maxprediction

    # for all the nodes get a prediction
    for node in nodes:
        # Base case: we've reached a leaf
        if isinstance(node, Leaf):
            return node.maxprediction

        # get all the classification and and choose the majority vote
        if node.question.match(row, header):
            classifications.append(classify1d(row, node.true_branch, header))
        else:
            classifications.append(classify1d(row, node.false_branch, header))

    # return the majority voted classification
    return classifications


# build the trees for the data
def buildAlltree(data):

    # Build all the decision trees in the hypothesis space
    try:
        with open("allTreesCOOR1D.pickle", 'rb') as f:
            my_trees = pickle.load(f)
    except:
        my_trees = build_tree(data, 1)
        # dump all the Trees made
        pickle.dump(my_trees, open("allTreesCOOR1D.pickle", "wb"))

    return my_trees


# print all the trees
def printAllTree(trees):

    # print the tree
    print("The Decision Stumps")
    for count, t in enumerate(trees):
        print("New tree: ", count)
        print_tree(t)
        # print(list(classify(data_train[header[0:22]].values[0], t, header))[0])
        print("\n")


# helper function for array equality
def isArrayEqual(arr1, arr2):

    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False

    return True


# get the exponential loss
def getLoss(dataX, dataY, trees, alpha_learner):
    loss = 0

    # for all the data points calculate the exponential loss
    for m, row in enumerate(dataX.values):
        combined_hypo = 0

        # value of the combined hypothesis
        for t, tree in enumerate(alpha_learner):
            # is the data X a list of list or a single list
            combined_hypo += alpha_learner[t] * classify(dataX.iloc[m], trees[t])

        # calculate the loss
        loss += np.exp(-1 * dataY.iloc[m] * combined_hypo)

    return loss


# get the new alpha
def getAlpha(dataX, dataY, trees, alpha_learner, curr_alpha_index):

    # calculating the new alpha
    corr_classfy = 0
    incorr_classfy = 0

    # calculate the total prediction
    for m, row in enumerate(dataX.values):
        combined_hypo = 0

        # value of the combined hypothesis
        for t, alpha in enumerate(alpha_learner):
            if t != curr_alpha_index:
                # is the data X a list of list or a single list
                combined_hypo += alpha_learner[t] * classify(dataX.iloc[m], trees[t])

        # does current tree classifies the point correctly
        if dataY.iloc[m] == classify(row, trees[curr_alpha_index]):
            corr_classfy += math.exp(-1 * dataY.iloc[m] * combined_hypo)
        else:
            incorr_classfy += math.exp(-1 * dataY.iloc[m] * combined_hypo)

    # calculate the new alpha for the learner
    return 0.5 * np.log(float(corr_classfy) / float(incorr_classfy))


# coordinate descent algorithm
def coordinateDescent(trees, data, alphas, header):

    # the new alphas for all the learners
    alphas = copy.deepcopy(alphas)

    # continue while the alphas do not converge
    while True:

        # get the exponential loss
        loss_learner = getLoss(data[header[0:22]], data["Y"], trees, alphas)
        print('\n\nLoss : ', loss_learner)

        for t, alpha in enumerate(alphas):
            # calculating the new alpha
            alphas[t] = getAlpha(data[header[0:22]], data["Y"], trees, alphas, t)

        # print the alpha and the new alpha
        print('New alpha', len(alphas), 'New alpha: \n', alphas)

        # break condition and calculate the final loss
        if loss_learner - getLoss(data[header[0:22]], data["Y"], trees, alphas) < 1:
            loss_learner = getLoss(data[header[0:22]], data["Y"], trees, alphas)
            break

    # print the current loss, alpha and the new alpha
    print('FINAL Loss : ', loss_learner)
    print('FINAL alpha: \n', alphas)

    # return the final alpha and corresponding loss
    return alphas, loss_learner


# get the prediction
def getPrediction(data, trees, alphas):
    pred_y = []

    for row in data.values:
        final = 0.

        # get the wighted prediction
        for t, final_a in enumerate(alphas):
            final += final_a * classify(row, trees[t])

        pred_y.append(np.sign(final))

    return pred_y


def main():
    # load the data
    data_train, header = getData("../heart_train.data")

    my_trees = buildAlltree(data_train)

    # print the trees
    printAllTree(my_trees)

    # print the data
    print(data_train)

    # initialize the alphas
    alphas = [0] * len(my_trees)

    # get the final alphas and the exp loss
    final_alphas, exp_loss = coordinateDescent(my_trees, data_train, alphas, header)

    print("Loss: ", exp_loss, " Final Alpha: ", final_alphas)

    # the FINAL prediction
    # TESTING DATA
    data_test, header = getData("../heart_test.data")

    actual_y = data_test["Y"]
    final_pred_y = getPrediction(data_test, my_trees, final_alphas)

    print("FINAL Acc test: ", accuracy_score(actual_y, final_pred_y), "\n\n")


if __name__ == '__main__':
    main()