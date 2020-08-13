# Kunal Mukherjee
# 2/17/2019
# CS 6375

# import the libraries
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import operator

# load a the data
mush_train = pd.read_csv("mush_train.data")
header = mush_train.keys().tolist()


# return the unique values for a column in a data
def unique_vals(data, colName):

    return data[colName].value_counts().keys().tolist()


# return the unique samples and their occurrence count in the dataset
def label_counts(data):
    values = data["Y"].value_counts().tolist()
    keys = data["Y"].value_counts().keys().tolist()
    return dict(zip(keys, values))


# Test if a value is numeric
def is_numeric(value):

    return isinstance(value, int) or isinstance(value, float)


# test usage [q = Question(header.index("X0"), 'x')]
class Question:
    # the Question is used to partition a dataset.

    def __init__(self, column, value):
        self.column = column
        self.value = value

    # The 'match' method is used to check
    # the feature value in an given row
    # with the feature value stored in the question.
    # question.match(row)
    def match(self, row):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = row[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


# Partition the dataset based on if a particular feature
# has an expected value or not
# [true_rows, false_rows = partition(mush_train, Question(0, "f"))]
def partition(data, question):

    # for each row in the dataset
    # check if the row matches the expected value of a given question
    true_rows, false_rows = [], []
    for row in data.values:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


# calculating entropy = h_y = sum(p(Y=y)log p(Y=y))
# current_uncertainty = entropy(mush_train)
def entropy(data):
    rows = data.values

    h_y = 0

    counts = label_counts(data)
    for lbl in counts:
        h_y -= (counts[lbl] / float(len(rows))) * (np.log10(counts[lbl] / float(len(rows))))

    return h_y


# calculate the information gain of the current node
# the its branches
# [i = info_gain(true_rows, false_rows, current_uncertainty)]
def info_gain(left, right, current_uncertainity):
    # Information Gain: larger IG less uncertainty
    # The uncertainty of the starting node, minus the weighted impurity of
    # two child nodes.

    # left probability
    p = float(len(left)) / (len(left) + len(right))

    return current_uncertainity - \
           p * entropy(pd.DataFrame(left, columns=header)) - (1 - p) * entropy(pd.DataFrame(right, columns=header))


# An algorithm to find the best split
# [best_gain, best_question = find_best_split(mush_train)]
def find_best_split(data):

    # We want to find the best question to ask
    # So, ask question for all the features and its values
    # calculate the information gain for all the question
    # choose the question with the largest information gain

    # calculate the uncertainty of the data
    current_uncertainty = entropy(data)

    best_gain = 0  # the best information gain
    best_question = None  # store the question that has the largest IG
    n_features = len(data.values[0]) - 1  # remove the label column

    for col in range(n_features):  # for each feature

        # get unique val for each column
        values = unique_vals(data, header[col])

        # for each of the unique value
        for val in values:  # for each value

            # make the question
            question = Question(col, val)

            # try splitting the dataset based on the question
            true_rows, false_rows = partition(data, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # keep track of the best question and the IG it provided
            if gain >= best_gain:
                best_gain, best_question = gain, question

    # returns the question that gives the best split
    return best_gain, best_question


class Leaf:
    # leaf node holds the label for the data that is left
    def __init__(self, data):
        self.predictions = label_counts(data)


class Decision_Node:
    # Decision node contains a question
    # It contains the data set that answered true
    # It contains the data set that answered false
    # It contains the IG for that node
    def __init__(self, question, true_branch, false_branch, gain):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.gain = gain


# Bilds the tree
# [my_tree = build_tree(mush_train)]
def build_tree(data):

    # Want to partition the dataset on each of the unique attribute
    # get the information gain
    # and return the question that produces the highest gain
    # SO: we get the best split
    gain, question = find_best_split(data)

    # Base case: no info gain
    # no split will result in a better classfication
    # so it is a leaf
    if gain == 0:
        return Leaf(data)

    # a good feature and its value (question) has been found that
    # partitions the data
    true_rows, false_rows = partition(data, question)

    # Recursively build the true branch, data that has the value for the chosen feature
    true_branch = build_tree(pd.DataFrame(true_rows, columns=header))

    # Recursively build the false branch, data that does not have the value for the chosen feature
    false_branch = build_tree(pd.DataFrame(false_rows, columns=header))

    # Return a Decision node.
    # This records the best Question (feature / value) to ask at this point,
    # as well as the branches resulting from the question
    return Decision_Node(question, true_branch, false_branch, gain)


# prints the tree
# [print_tree(my_tree)]
def print_tree(node, spacing=""):

    # Base case: the node is a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    # It is a decision node
    # print the question and the gain
    print (spacing + str(node.question) + " Gain: " + str(node.gain))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


# print the forest
def print_tree1d(nodes, spacing=""):

    for node in nodes:
        # Base case: we've reached a leaf
        if isinstance(node, Leaf):
            print(spacing + "Predict", node.predictions)
            return

        # Print the question at this node
        print(spacing + str(node.question) + " Gain: " + str(node.gain))

        # Call this function recursively on the true branch
        print(spacing + '--> True:')
        print_tree(node.true_branch, spacing + "  ")

        # Call this function recursively on the false branch
        print(spacing + '--> False:')
        print_tree(node.false_branch, spacing + "  ")


# Classifies the row based on the tree's root node given
# [classify(mush_train.values[2], my_tree)]
def classify(row, node):

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch
    # Use the question(feature / value) the node
    # to select which branch to follow
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


# classify the row, based on all the question for a given feature
def classify1d(row, nodes):
    # get the classification for an row
    # using a list of nodes
    classifications = []

    if isinstance(nodes, Leaf):
        return nodes.predictions

    # for all the nodes get a prediction
    for node in nodes:
        # Base case: we've reached a leaf
        if isinstance(node, Leaf):
            return node.predictions

        # get all the classification and and choose the majority vote
        if node.question.match(row):
            classifications.append(classify1d(row, node.true_branch))
        else:
            classifications.append(classify1d(row, node.false_branch))

    # return the majority voted classification
    return classifications


# Prints the leaf as a percentage
def print_leaf(counts):

    total = sum(counts.values()) * 1.0
    probability = {}
    for lbl in counts.keys():
        probability[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probability


# Prints the leaf as a percentage
def print_leafnd(counts):
    probability = {}
    for c in counts:
        for count in c:
            if isinstance(count, dict):
                total = sum(count.values()) * 1.0
                for lbl in count.keys():
                    probability[lbl] = str(int(count[lbl] / total * 100)) + "%"
    return probability


# Decision Tree algorithm for Classification
def decision_tree_classification():
    global header

    # load the data
    mush_train = pd.read_csv("mush_train.data")

    # header manipulation
    cols = mush_train.columns.tolist()
    cols = cols[1:23] + cols[0:1]
    header = cols

    # data manipulation based on the header
    mush_train = mush_train[cols]

    # Build the decision tree based on the data
    my_tree = build_tree(mush_train)
    # print the tree
    print_tree(my_tree)

    # TRAINING DATA
    pred_y = []
    actual_y = mush_train["Y"]

    # for each row of the training data, predict the label
    for row in mush_train.values:
        # print("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, my_tree))))
        pred_y.append(list(print_leaf(classify(row, my_tree)).keys())[0])

    print("Acc train", accuracy_score(actual_y, pred_y))

    # TESTING DATA
    mush_test = pd.read_csv("mush_test.data")

    # move label to the last column
    mush_test = mush_test[cols]

    pred_y = []
    actual_y = mush_test["Y"]

    # for each row of the testing data, predict the label
    for row in mush_test.values:
        # print("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, my_tree))))
        pred_y.append(list(print_leaf(classify(row, my_tree)).keys())[0])

    print("Acc test", accuracy_score(actual_y, pred_y))


##### PROBLEM 3.3 #####

# Find all the question for a given column
def find_all_question(data, attrName):
    questions = []
    vals = unique_vals(data, attrName)

    for val in vals:
        questions.append(Question(header.index(attrName), val))

    return questions


# build the forest for an attribute
def build_tree1d(data, attrName):

    # Find all the question possible for the given attribute
    questions = find_all_question(data, attrName)

    decision_nodes = []

    # create a decision tree for each of the given node
    for question in questions:
        true_rows, false_rows = partition(data, question)

        # the depth is one, so it will have only leaves
        # the true leaf
        true_leaf = Leaf(pd.DataFrame(true_rows, columns=header))

        # the false leaf
        false_leaf = Leaf(pd.DataFrame(false_rows, columns=header))

        # calculate the Uncertainty and IG
        # for a particular question
        current_uncertainty = entropy(data)
        gain = info_gain(true_rows, false_rows, current_uncertainty)

        # contains the root node for the possible questions
        decision_nodes.append(Decision_Node(question, true_leaf, false_leaf, gain))

    # Return all the possible of one split for the particular attribute
    return decision_nodes


# use majority vote for many classificiaiton
def overall_class(classification):
    e = 0
    p = 0

    for count, clas in enumerate(classification):
        if 'e' in print_leaf(clas):
            e += int(print_leaf(clas)['e'].rstrip("%"))
        if 'p' in print_leaf(clas):
            p += int(print_leaf(clas)['p'].rstrip("%"))

    p /= len(classification)
    e /= len(classification)
    # print('p ', p, 'e ', e)

    if p >= e:
        return 'p'
    else:
        return 'e'


def question3():
    global header

    # data pre-processing
    mush_train = pd.read_csv("mush_train.data")

    cols = mush_train.columns.tolist()
    cols = cols[1:23] + cols[0:1]
    header = cols

    mush_train = mush_train[cols]

    h_Accurs = []
    info_gains = []

    # for all the features build a a tree of depth one using all the questions
    # use it to classify data points using majority vote if a mix of labels found
    for h in range(len(header) - 1):
        # Build a 1 depth tree
        my_tree = build_tree1d(mush_train, header[h])  # "X0"

        info_gain = 0

        for node in my_tree:
            info_gain += node.gain
        # print_tree1d(my_tree)

        # TRAINING
        pred_y = []
        actual_y = mush_train["Y"]

        for row in mush_train.values:
            # print("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, my_tree))))
            pred_y.append(overall_class(classify1d(row, my_tree)))

        pred_y = np.asarray(pred_y)

        print("Atrribute: ", header[h], 'info gain: ', info_gain, "Acc train", accuracy_score(actual_y, pred_y))

        h_Accurs.append(accuracy_score(actual_y, pred_y))
        info_gains.append(info_gain)

    # print the max information gain and the max accuracy
    print("IG: ", header[info_gains.index(max(info_gains))], max(info_gains))
    print("Acc: ", header[h_Accurs.index(max(h_Accurs))], max(h_Accurs))


def main():
    decision_tree_classification()
    question3()


if __name__ == '__main__':
    main()



#question3()
