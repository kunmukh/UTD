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

    all_label = list(itertools.product([0, 1], repeat=2))

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
        print (spacing + "Predict", node.predictions, "Max Predict", node.maxprediction)
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
            print(spacing + "Predict", node.predictions, "Max Predict", node.maxprediction)
            return

        # Print the question at this node
        print(spacing + str(node.question))

        # Call this function recursively on the true branch
        # print(spacing + '--> True:')
        print_tree(node.true_branch, spacing + 'True  --> :' + "  ")

        print_tree(node.false_branch, spacing + 'False --> :' + "  ")


# Classifies the row based on the tree's root node given
# [classify(mush_train.values[2], my_tree)]
def classify(row, node, header):

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.maxprediction

    # Decide whether to follow the true-branch or the false-branch
    # Use the question(feature / value) the node
    # to select which branch to follow
    if node.question.match(row, header):
        return classify(row, node.true_branch, header)
    else:
        return classify(row, node.false_branch, header)


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


def main():
    # load the data
    data_train = pd.read_csv("../heart_train.data")
    # load only 5 data
    # mush_train = data_train[:15]

    # header manipulation
    cols = data_train.columns.tolist()
    cols = cols[1:23] + cols[0:1]
    header = cols

    # data manipulation based on the header
    data_train = data_train[cols]

    # Build the decision tree based on the data
    try:
        with open("allTrees1D.pickle", 'rb') as f:
            my_trees = pickle.load(f)
    except:
        my_trees = build_tree(data_train, 1)
        # dump all the Trees made
        pickle.dump(my_trees, open("allTrees1D.pickle", "wb"))

    # print the tree
    # print_tree1d(my_trees)
    '''print("The Decision Stumps")
    for count, t in enumerate(my_trees):
        print("New tree: ", count)
        print_tree(t)
        print(list(classify(data_train[header[0:22]].values[0], t, header))[0])
        print("\n")'''

    # move label to the last column
    data_train = data_train[header]

    # initializing the weight for the first round
    data_train['w'] = pd.Series(1 / data_train.shape[0], index=data_train.index)

    print(data_train)

    NUM_BOOST = 20
    prediction_alpha_h = []

    # for the number of boosting:
    for boost in range(0, NUM_BOOST):
        # re-initialize best weight and error
        best_weight_error = 100
        best_stump = 100

        for count_tree, t in enumerate(my_trees):
            pred_y = []
            weighted_error = 0

            # for each tree calculate the weighted error
            for count, row in enumerate(data_train[header[0:22]].values):

                if data_train["Y"][count] != list(classify(row, t, header))[0]:
                    weighted_error += data_train["w"][count]

                pred_y.append(list(classify(row, t, header)))

            # print(pred_y)
            # print("Acc test: Tree: ", count_tree, "Acc: ", accuracy_score(actual_y, pred_y),
            #       "e: ", weighted_error, "\n")

            # if the weighted error is small than the best, update
            if weighted_error < best_weight_error:
                best_weight_error = weighted_error
                best_stump = count_tree

        # compute alpha
        alpha = 0.5 * np.log((1 - best_weight_error)/(best_weight_error))

        prediction_alpha_h.append([alpha, best_stump])

        print_tree(my_trees[best_stump])
        print("Best Acc Tree: ", best_stump,
              "e: ", best_weight_error,
              "alpha: ", alpha,
              "boost: ", boost, "\n\n")

        # update the weights
        new_weights = []
        for count, (row, w) in enumerate(zip(data_train[header[0:22]].values, data_train["w"].values)):
            # compute the new weights
            new_weights.append((w
                                * math.exp(-1 * data_train["Y"][count] *
                                           list(classify(row, my_trees[best_stump], header))[0]
                                * alpha)) /
                               (2 * math.sqrt(best_weight_error * (1-best_weight_error))))

        data_train["w"] = new_weights
        print(data_train)

    print(prediction_alpha_h)

    # the FINAL prediction
    # TESTING DATA
    data_test = pd.read_csv("../heart_test.data")

    # move label to the last column
    data_test = data_test[header]

    actual_y = data_test["Y"]
    final_pred_y = []

    for row in data_test[header[0:22]].values:
        final = 0.

        # get the wighted prediction
        for final_a_h in prediction_alpha_h:
            final += final_a_h[0] * list(classify(row, my_trees[final_a_h[1]], header))[0]

        final_pred_y.append(np.sign(final))

    # print(final_pred_y)
    print("FINAL Acc test dataset: ", accuracy_score(actual_y, final_pred_y), "\n\n")


if __name__ == '__main__':
    main()