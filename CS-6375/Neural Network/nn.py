import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import tensorflow as tf


def main():
    dataset = pd.read_csv('example.data')

    X = dataset.iloc[:, :10].values
    y = dataset.iloc[:, 10:11].values

    print(X)
    print(y)

    '''sc = StandardScaler()
    X = sc.fit_transform(X)

    print(X)
    print(y)

    ohe = OneHotEncoder()
    y = ohe.fit_transform(y).toarray()

    print(X)
    print(y)'''

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    model = Sequential()
    model.add(Dense(4, input_dim=10, activation='relu'))
    model.add(Dense(2, activation='relu'))
    model.add(Dense(1, activation='relu'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    history = model.fit(X_train, y_train, validation_split=0.2, shuffle=True,
                        epochs=100, batch_size=64)

    pred = model.predict(X_test)
    # print(pred)
    y_pred = list()
    for i in range(len(pred)):
        y_pred.append(np.round(pred[i][0]))
    print(y_pred)
    print(np.ndarray.flatten(y_test))

    a = accuracy_score(y_pred, y_test)
    print('Accuracy is:', a * 100)

    i = 0
    for layer in model.layers:
        print('\nlayer:', i, 'weights:\n',  layer.get_weights())
        i += 1


if __name__ == '__main__':
    main()