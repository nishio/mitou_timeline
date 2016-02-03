import numpy as np
from sklearn.linear_model import LogisticRegression
from scipy.stats import logistic

import features
fs = features.POSITIVE + features.NEGATIVE
M = len(fs)

def make_feature_matrix(lines):
    N = len(lines)
    X = np.zeros((N, M))
    for i, line in enumerate(lines):
        X[i, :] = [f in line for f in fs]
    return X

def learn(penalty='l2'):
    pos_x = file('positive.txt').readlines()
    neg_x = file('negative.txt').readlines()#[:len(pos_x)]
    N = len(pos_x) + len(neg_x)

    X = np.zeros((N, M))
    Y = np.zeros((N, ))

    for i, line in enumerate(pos_x):
        X[i, :] = [f in line for f in fs]
        Y[i] = 1

    offset = len(pos_x)
    for i_, line in enumerate(neg_x):
        i = offset + i_
        X[i, :] = [f in line for f in fs]
        Y[i] = 0

    lr = LogisticRegression(penalty=penalty)
    lr.fit(X, Y)
    return lr

def feature_compression():
    lr = learn(penalty='l1')
    scores = list(sorted(zip(lr.coef_.ravel(), fs), reverse=True))
    for w, t in scores:
        print w, t

if __name__ == '__main__':
    feature_compression()
