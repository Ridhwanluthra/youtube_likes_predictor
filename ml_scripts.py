from pymongo import MongoClient
import numpy as np
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn import preprocessing
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import pydotplus
from sklearn.ensemble import AdaBoostClassifier


def fib(n):
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
    return a

def get_fib(max_val):
    i = 2
    n = 0
    arr = []
    while n <= 12863115:
        n = fib(i)
        arr.append(n)
        i += 1
    return arr

def find_none_count(dic):
    none_count = {}
    for key in dic[0]:
        none_count[key] = 0
    for i in range(dic.count()):
        for key in dic[i]:
            if dic[i][key] == None:
                none_count[key] += 1
    return none_count

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print('started models')
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    nn = MLPRegressor(hidden_layer_sizes=(100,100,100,), activation='relu')
    print('started trining')
    y_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)
    print('rbf done')
    print('rbf...;---')
    print('mean_squared_error', metrics.mean_squared_error(y_test, y_rbf))
    print('r2_score', metrics.r2_score(y_test, y_rbf))
    # for i in range(len(y)):
    #     print(y[i], ':', y_rbf[i])

    lw = 2
    xx = np.arange(len(y_test))
    plt.scatter(xx, y_test, color='darkorange', label='data')
    plt.hold('on')
    plt.scatter(xx, y_rbf, color='navy', lw=lw, label='RBF model')
    # plt.plot(X, y_nn, color='c', lw=lw, label='nn model')
    # plt.plot(X, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
    plt.xlabel('data')
    plt.ylabel('target')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()
    # y_lin = svr_lin.fit(X, y).predict(X)
    # print('lin done')
    # print('lin', svr_lin.score(X, y))
    # y_poly = svr_poly.fit(X, y).predict(X)
    # print('poly done')
    # print('poly....;--', svr_poly.score(X, y))
    y_nn = nn.fit(X_train, y_train).predict(X_test)
    print('ANN...')
    print('mean_squared_error', metrics.mean_squared_error(y_test, y_nn))
    print('r2_score', metrics.r2_score(y_test, y_nn))
    # for i in range(len(y)):
    #     print(y[i], ':', y_nn[i])

    lw = 2
    xx = np.arange(len(y_test))
    plt.scatter(xx, y_test, color='darkorange', label='data')
    plt.hold('on')
    # plt.plot(xx, y_rbf, color='navy', lw=lw, label='RBF model')
    plt.scatter(xx, y_nn, color='c', lw=lw, label='ann model')
    # plt.plot(X, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
    plt.xlabel('data')
    plt.ylabel('target')
    plt.title('Neural Network Regression')
    plt.legend()
    plt.show()
    # TODO: ADD ADABOOST


def train_classification_models(X, y):
    X = preprocessing.normalize(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print('started models')
    svr_rbf = SVC(kernel='rbf', C=1e3, gamma=0.1)
    svr_lin = SVC(kernel='linear', C=1e3)
    svr_poly = SVC(kernel='poly', C=1e3, degree=2)
    nn = MLPClassifier(hidden_layer_sizes=(100,100,), activation='relu')
    print('started trining')

    y_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)
    print('rbf done')
    print('rbf...;---', metrics.f1_score(y_test, y_rbf, average='weighted'))

    # y_lin = svr_lin.fit(X_t;trics.f1_score(y_test, y_poly))

    y_nn = nn.fit(X_train, y_train).predict(X_test)
    print('ann done')
    print('ann:---', metrics.f1_score(y_test, y_nn, average='weighted'))

def random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # clf = RandomForestClassifier()
    clf = tree.DecisionTreeClassifier()
    # clf = AdaBoostClassifier()
    clf = clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    dot_data = tree.export_graphviz(clf, out_file=None,
                                        max_depth=None,
                                        filled=True, rounded=True,  
                                        special_characters=True) 
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf('all.pdf')

    print(metrics.f1_score(y_test, y_pred, average='weighted'))

if __name__ == '__main__':

    client = MongoClient()
    db = client.precog

    dic = db.features.find()

    y = []
    X = []

    for i in range(dic.count()):
        # create a array for 1 training example
        x = []
        ignore = False
        for key in dic[i]:
            # ignore id key
            if key == '_id':
                continue
            val = dic[i][key]
            # take likes as the label the rest in x
            if key == 'likes':
                if val == None:
                    ignore = True
                else:
                    # val = int(np.log10(val))
                    y.append(val)
            else:
                if val == None:
                    x.append(0)
                else:
                    x.append(val)
        # add 1 training example to the mix
        if ignore == False:
            X.append(x)

    print(len(X), len(y))
    # print(len(set(y)))
    # print(min(y), max(y))
    # print(get_fib(max(y)))
    y = np.digitize(y, get_fib(max(y)))
    # for i in range(len(inds)):
    #     print(inds[i])
    # from sklearn.preprocessing import scale
    # y = scale(y)
    # for i in range(len(y)):
    #     print(y[i])
    random_forest(X,y)

    # cov = np.cov(np.transpose(X))
    # from decimal import Decimal
    # temp = []
    # for i in range(len(cov)):
    #     a = []
    #     for j in range(len(cov[0])):
    #         a.append(round(Decimal(cov[i][j]), 2))
    #     temp.append(a)
    # print(temp)
            # print(cov[i][j])
        # print(cov[i])

    # pca = PCA()
    # pca.fit(X)
    # print(pca.explained_variance_)

    # for i in range(len(cov)):
    #     print(temp[i])

    

    # for i in range(len(X)):
    #     print(X[i])
    train_classification_models(X,y)

    # print(find_none_count(dic))