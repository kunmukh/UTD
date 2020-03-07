# Kunal Mukherjee
# Gensim-Autoencoder: outlier detector
# 3/6/20

# import statements
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

import smart_open
import gensim
import numpy as np
import pandas as pd
import pprint

# Path to dataset
# Set file names for train and test data
# lee_train_file = '../data/lee_train.txt'
# lee_test_file = '../data/lee_test.txt'

lee_train_file = '../data/adult_train.txt'
lee_test_file = '../data/adult_test.txt'
# lee_test_file = '../data/child_test.txt'


# function to create a taggedDocument or tokenzie a Document
def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


# generate the training and testing corpus
def dataProcessing(train_file, test_file):
    # generate the training and testing corpus
    train_corpus = list(read_corpus(train_file))
    test_corpus = list(read_corpus(test_file, tokens_only=True))

    # print(pd.DataFrame(data=train_corpus))
    # print(pd.DataFrame(data=test_corpus))

    return train_corpus, test_corpus


# generate the feature for the input doc
def DoctoVecFeatureGenerator(train_corpus):
    # generate the model for the training document
    model = gensim.models.doc2vec.Doc2Vec(min_count=2, epochs=40)
    model.build_vocab(train_corpus)

    # summarize the loaded model
    # print("model:", model)

    # get the words form the dict
    # words = list(model.wv.vocab)
    # print("Words: ", words)

    # access feature vector for one word
    # each word has 100 features
    # print("Vec for 'sentence'", model['sentence'])

    # access count of feature vector for one word
    # print(model.wv.vocab['sentence'].count)

    # print the vocab
    # pprint.pprint(model.wv.vocab)

    # get the feature vector from the training data set
    feature_vec_train = model[model.wv.vocab]

    # each word has 100 features
    # print(" Feature Training Vector: \n", pd.DataFrame(data=feature_vec_train))

    return feature_vec_train, model


# create the auto-encoder
def autoEncoder(feature_vec_train):
    # NORMALIZE THE DATA AND BUILD AN AUTOENCODER

    # normalize the feature
    # scaler = MinMaxScaler()
    # scaled_seqs = scaler.fit_transform(feature_vec_train)

    # no need to scale for feature vec in doc2vec
    # divide the data into train and test
    X_train, X_test = train_test_split(feature_vec_train, test_size = 0.20)

    # SETTING UP THE AUTO-ENCODER
    # TODO: test this hyper parameters
    input_dim = X_train.shape[1]  # features
    encoding_dim = input_dim
    hidden_dim = int(encoding_dim / 2)

    nb_epoch = 30
    batch_size = 128
    learning_rate = 0.1

    input_layer = Input(shape=(input_dim,))

    encoder = Dense(encoding_dim, activation="tanh",
                    activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoder = Dense(hidden_dim, activation="relu")(encoder)
    decoder = Dense(encoding_dim, activation='relu')(encoder)
    decoder = Dense(input_dim, activation='tanh')(decoder)

    # FIT THE MODEL

    autoencoder = Model(inputs=input_layer, outputs=decoder)

    autoencoder.compile(optimizer='adam',
                        loss='mean_squared_error',
                        metrics=['accuracy'])

    checkpointer = ModelCheckpoint(filepath="model_seqs2.h5",
                                   verbose=0,
                                   save_best_only=True)

    tensorboard = TensorBoard(log_dir='./logs',
                              histogram_freq=0,
                              write_graph=True,
                              write_images=True)

    history = autoencoder.fit(X_train, X_train,
                              epochs=nb_epoch,
                              batch_size=batch_size,
                              shuffle=True,
                              validation_data=(X_test, X_test),
                              verbose=1,
                              callbacks=[checkpointer, tensorboard]).history
    # Print the minimum loss
    print('\n' + f'Min Loss:{np.min(history["loss"])}' + '\n')

    # plot the loss v epocs graph
    plt.subplot(1, 2, 1)
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')


# infer the feature for the test_corpus from the doc2vec model
def DoctoVecFeatureInfer(doc2vecmodel, test_corpus):
    num_features = 100

    # extract the feature vector for each corpus in the test corpus
    feature_vec_test = np.empty((0, num_features))
    for i, corpus in enumerate(test_corpus):
        feature_vec_test = np.append(feature_vec_test, [doc2vecmodel.infer_vector(corpus)], axis=0)

    print(" Feature Test Vector: \n", pd.DataFrame(data=feature_vec_test).head())
    # print("Test Vec", np.asarray(feature_vec_test).shape)

    # normalize it
    # feature_vec_test = MinMaxScaler().fit_transform(feature_vec_test)
    # print(feature_vec_test)

    return feature_vec_test


# predict the in-lier and out-lier
def prediction(doc2vecmodel, test_corpus, feature_vec_train):
    # PREDICTION STEP
    autoencoder = load_model('model_seqs2.h5')

    # Testing the model
    feature_vec_test = DoctoVecFeatureInfer(doc2vecmodel, test_corpus)

    # combine test and train feature vec
    feature_vec = np.concatenate((feature_vec_train, feature_vec_test), axis=0)

    # predict it
    predicted = autoencoder.predict(feature_vec)

    return feature_vec, predicted


# use mean sq. error to calculate anomaly
def meanSqError (feature_vec, predicted_vec):
    # get the error term
    mse = np.mean(np.power(feature_vec - predicted_vec, 2), axis=1)

    # now add them to our data frame
    seqs_ds = pd.DataFrame(data={'line #': [i for i in range(0, feature_vec.shape[0])]})

    seqs_ds['MSE'] = mse

    print(seqs_ds)

    # getting the threshold
    # TODO: test threshold hyper parameters org:0.9997
    mse_threshold = np.quantile(seqs_ds['MSE'], 0.997)
    print('\n' + f'MSE 0.9997 threshold:{mse_threshold}' + '\n')

    # updating the MSE Outlier
    seqs_ds['MSE_Outlier'] = 0
    seqs_ds.loc[seqs_ds['MSE'] > mse_threshold, 'MSE_Outlier'] = 1

    print(seqs_ds)

    print('\n' + f"Num of MSE outlier:{seqs_ds['MSE_Outlier'].sum()}" + '\n')

    feature_vec_inlier_indices  = seqs_ds['MSE_Outlier'] <= 0
    feature_vec_outlier_indices = seqs_ds['MSE_Outlier'] > 0

    feature_vec_inlier = np.asarray(feature_vec)[feature_vec_inlier_indices]
    feature_vec_outlier = np.asarray(feature_vec)[feature_vec_outlier_indices]

    print("Inlier or Outlier:")
    print("% of Inlier :", len(feature_vec_inlier) / len(seqs_ds['MSE_Outlier']))
    print("% of Outlier:", len(feature_vec_outlier) / len(seqs_ds['MSE_Outlier']))

    return feature_vec_inlier, feature_vec_outlier


#plot the TSNE plot
def plotTSNE(feature_vec_train, feature_vec_inlier, feature_vec_outlier):
    # Plot using TSNE
    plt.subplot(1, 2, 2)
    plt.title('T-SNE')

    tsne = TSNE(n_components=2, perplexity=50, n_iter=300)

    # plotting Training feature vector using TSNE
    tsne_results_train = tsne.fit_transform(feature_vec_train)
    plt.scatter(tsne_results_train[:, 0], tsne_results_train[:, 1], c='black')

    # in-lier feature vector
    tsne_results_vec = tsne.fit_transform(feature_vec_inlier)
    plt.scatter(tsne_results_vec[:, 0], tsne_results_vec[:, 1], c='blue')

    # out-lier feature vector
    if len(feature_vec_outlier) > 1:
        tsne_results_vec = tsne.fit_transform(feature_vec_outlier)
        plt.scatter(tsne_results_vec[:, 0], tsne_results_vec[:, 1], c='red')


# the main program
def main():

    # get the training and testing data
    train_corpus, test_corpus = dataProcessing(lee_train_file, lee_test_file)
    # generate the doc2vec model and get the feature for the training
    feature_vec_train, model = DoctoVecFeatureGenerator(train_corpus)
    # encode the feature of the training document
    autoEncoder(feature_vec_train)
    # get the prediction of the inlier and outlier from the test_corpus
    feature_vec, pred = prediction(model, test_corpus, feature_vec_train)
    # get the meanSqError from the feature_vec_test, predicition_vec, feature_vec_train
    feature_vec_inlier, feature_vec_outlier = meanSqError(feature_vec, pred)
    # plot the TSNE
    plotTSNE(feature_vec_train, feature_vec_inlier, feature_vec_outlier)

    # plot the outlier
    plt.show()


if __name__ == '__main__':
    main()