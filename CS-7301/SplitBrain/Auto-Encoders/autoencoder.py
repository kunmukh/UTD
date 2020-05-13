# Kunal Mukherjee
# Auto-Encoder: https://github.com/a-agmon/experiments/blob/master/Sequence_Anomaly_Detection-NN.ipynb
# 3/6/20

# import statements
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

rcParams['figure.figsize'] = 12, 6

# GENERATING SEQUENCE MODEL
first_letters = 'ABCDEF'
second_numbers = '120'
last_letters = 'QWOPZXML'


# returns a string of the following format: [4 letters A-F][1 digit 0-2][3 letters QWOPZXML]
def get_random_string():
    str1 = ''.join(random.choice(first_letters) for i in range(4))
    str2 = random.choice(second_numbers)
    str3 = ''.join(random.choice(last_letters) for i in range(3))
    return str1 + str2 + str3


# generate a random string
print(get_random_string())

# get 25,000 sequences of this format
random_sequences = [get_random_string() for i in range(25000)]
# print only the first five
print(random_sequences[1:5])

# Build the char index that we will use to encode seqs to numbers
char_index = '0abcdefghijklmnopqrstuvwxyz'
char_index += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
char_index += '123456789'
char_index += '().,-/+=&$?@#!*:;_[]|%⸏{}\"\'' + ' ' + '\\'

char_to_int = dict((c, i) for i, c in enumerate(char_index))
int_to_char = dict((i, c) for i, c in enumerate(char_index))

print('\nchar->int: \n', char_to_int)
print('\nint->char: \n', int_to_char)


# function that convert a char seqs to numbers seqs
# pad zeros for features
def encode_sequence_list(seqs, feat_n=0):
    encoded_seqs = []

    for seq in seqs:
        encoded_seq = [char_to_int[c] for c in seq]
        encoded_seqs.append(encoded_seq)

    if feat_n > 0:
        encoded_seqs.append(np.zeros(feat_n))

    return pad_sequences(encoded_seqs, padding='post')


# decode a sequence to characters
def decode_sequence_list(seqs):
    decoded_seqs = []

    for seq in seqs:
        decoded_seq = [int_to_char[i] for i in seq]
        decoded_seqs.append(decoded_seq)

    return decoded_seqs


# add 4 anomalies to our list
random_sequences.extend(['XYDC2DCA', 'TXSX1ABC', 'RNIU4XRE', 'AABDXUEI', 'SDRAC5RF'])

# save this to a dataframe
seqs_ds = pd.DataFrame(random_sequences)
print('\nsequences: \n', seqs_ds)

# encode each string seq to an integer array [[1],[5],[67]], [[45],[76],[7]
encoded_seqs = encode_sequence_list(random_sequences)
print('\nencoded: \n', encoded_seqs)

# mix everything up
np.random.shuffle(encoded_seqs)

# look at the word and its corresponding num mapping
print('\nrand seq: \n', random_sequences[10])
print('\nrand seq map: \n', encoded_seqs[10])

# PROCESS THE DATA AND BUILD AN AUTOENCODER

# normalize the data
scaler = MinMaxScaler()
scaled_seqs = scaler.fit_transform(encoded_seqs)
print('\nscaled seq\n', scaled_seqs[10])

# divite the data into train and test
X_train = scaled_seqs[:20000]
X_test = scaled_seqs[20000:]

# setting up autoencoder
input_dim = X_train.shape[1]  # features
encoding_dim = 8
hidden_dim = int(encoding_dim / 2)

nb_epoch = 30
batch_size = 128
learning_rate = 0.1

input_layer = Input(shape=(input_dim,))

encoder = Dense(encoding_dim, activation="tanh", activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(hidden_dim, activation="relu")(encoder)
decoder = Dense(encoding_dim, activation='relu')(encoder)
decoder = Dense(input_dim, activation='tanh')(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)

# FIT THE MODEL
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

'''history = autoencoder.fit(X_train, X_train,
                          epochs=nb_epoch,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(X_test, X_test),
                          verbose=1,
                          callbacks=[checkpointer, tensorboard]).history

# plot the result
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')'''
# plt.show()

# predicting step
autoencoder = load_model('model_seqs2.h5')
# print('\n' + f'Min Loss:{np.min(history["loss"])}' + '\n')

# PREDICT ON ALL THE SEQUENCE DATA

# encode all the data
encoded_seqs = encode_sequence_list(seqs_ds.iloc[:, 0])
# scale it
scaled_data = MinMaxScaler().fit_transform(encoded_seqs)

print(scaled_data)
print(scaled_data[0])
print(pd.DataFrame(data=scaled_data))

# predict it
predicted = autoencoder.predict(scaled_data)

# get the error term
mse = np.mean(np.power(scaled_data - predicted, 2), axis=1)

# now add them to our data frame
print(seqs_ds)
seqs_ds['MSE'] = mse

print(seqs_ds)

# getting the threshold
mse_threshold = np.quantile(seqs_ds['MSE'], 0.9999)
print('\n' + f'MSE 0.9997 threshold:{mse_threshold}' + '\n')

# getting the sequence
seqs_ds['MSE_Outlier'] = 0
seqs_ds.loc[seqs_ds['MSE'] > mse_threshold, 'MSE_Outlier'] = 1

print('\n' +  f"Num of MSE outlier:{seqs_ds['MSE_Outlier'].sum()}" + '\n')

print(seqs_ds.iloc[25000:])
