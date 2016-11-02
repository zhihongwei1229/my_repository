import sklearn
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import explained_variance_score, make_scorer

from sklearn.learning_curve import learning_curve
from sklearn.cross_validation import KFold

import matplotlib.pyplot as plt

#play with pyplt
if False:
    #generate Y axis values
    size = 10
    cv = KFold(size, shuffle=True)
    score = make_scorer(explained_variance_score)
    Y = np.reshape(np.random.normal(scale=2,size=size),(-1,1))
    # generate X axis values
    X = []
    for i in range(0, 10):
        X.append(i)
    print(X)
    print('~~~~~~~~~~~~~')
    print(Y)

    plt.ylim(-10, 10)
    plt.xlim(-1, 10)
    plt.ylabel("Y")
    plt.xlabel("X")
    plt.text(X[9], Y[9], r'training scores')
    plt.plot(X,Y)

    plt.show()


#Michine Learn cause testing
if True:
    size = 1000
    cv = KFold(size, shuffle=True)
    score = make_scorer(explained_variance_score)
    X = np.reshape(np.random.normal(scale=2,size=size),(-1,1))
    y = np.array([[1 - 2*x[0] +x[0]**2] for x in X])

    if False: #print X, y matrix
        print(X)
        print('~~~~~~~~~~~~~')
        print(y)
        exit(0)

    reg = LinearRegression()
    reg.fit(X, y)
    print("Regressor score: {:.4f}".format(reg.score(X, y)))

    train_sizes, train_scores, valid_scores = learning_curve(reg, X, y, train_sizes = [300, 500, 600], cv = cv, scoring=score)

    #plt.text(100, 1, r'training scores')
    #plt.plot(train_sizes, train_scores)

    plt.text(100, 2, r'test scores')
    plt.plot(train_sizes, valid_scores)

    plt.ylim(-.1, 1.1)
    plt.show()

    #print(train_scores)
    #print(valid_scores)
if False:
    X = pd.read_csv('titanic_data.csv')


    X = X._get_numeric_data()
    y = X['Survived']

    del X['Age'], X['Survived']

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=0)


    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    #sklearn.learning_curve(clf, X, y, )
    print (accuracy_score(clf.predict(X_test),y_test))
    print ("Decision Tree mean absolute error: {:.2f}".format(mse(clf.predict(X_test),y_test)))

    print ("Decision Tree F1 score: {:.2f}".format(f1_score(clf.predict(X_test),y_test)))
    #print(X_train)
    #print("~~~~~~~~~~~~~~~~~~")
    #print(y_train)