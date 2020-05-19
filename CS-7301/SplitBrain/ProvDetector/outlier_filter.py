import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn import svm
from sklearn.model_selection import train_test_split


def filter_outliers(train, test, model_name):
    data = train + test
    data = np.array(data)
    outliers_fraction = 0.05

    for i in range(3):
        if model_name == "LocalOutlierFactor":
            clf =  LocalOutlierFactor(contamination=outliers_fraction)
            pred = clf.fit_predict(data)
        elif model_name == "RobustCovariance":
            clf =  EllipticEnvelope(contamination=outliers_fraction)
            pred = clf.fit(data).predict(data)
        elif model_name == "SVM":
            clf = svm.OneClassSVM(nu=outliers_fraction, kernel="rbf", gamma=0.1)
            pred = clf.fit(data).predict(data)
        elif model_name == "Isolation Forest":
            clf =  IsolationForest(behaviour='new', contamination=outliers_fraction, random_state=42)
            pred = clf.fit(data).predict(data)
        data = data[pred==1]
    train, test = train_test_split(data, test_size=0.25) 
    return (train, test)

def filter_outliers2(train,  model_name):
    data = train
    data = np.array(data)
    outliers_fraction = 0.05

    for i in range(3):
        if model_name == "LocalOutlierFactor":
            clf =  LocalOutlierFactor(contamination=outliers_fraction)
            pred = clf.fit_predict(data)
        elif model_name == "RobustCovariance":
            clf =  EllipticEnvelope(contamination=outliers_fraction)
            pred = clf.fit(data).predict(data)
        elif model_name == "SVM":
            clf = svm.OneClassSVM(nu=outliers_fraction, kernel="rbf", gamma=0.1)
            pred = clf.fit(data).predict(data)
        elif model_name == "Isolation Forest":
            clf =  IsolationForest(behaviour='new', contamination=outliers_fraction, random_state=42)
            pred = clf.fit(data).predict(data)
        data = data[pred==1]
    return data
