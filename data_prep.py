import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score, make_scorer, precision_score
import datetime
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.ensemble import ExtraTreesClassifier


X = data.loc[:, data.columns != 'isFraud']
y = data['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


def prec(y_true, y_pre):
    return precision_score(y_true, y_pre)


score = make_scorer(prec, greater_is_better=True)

rf = RandomForestClassifier(max_features=0.5)

# param_grid = { "criterion" : ["gini", "entropy"],
#               "min_samples_leaf" : [1, 5, 10],
#               "min_samples_split" : [2, 4, 10, 12],
#               "n_estimators": [50, 100, 400, 700]}
param_grid = {"n_estimators": [50, 100, 150]}


gs = GridSearchCV(estimator=rf, param_grid=param_grid, scoring=score, cv=3, n_jobs=-1)
gs.fit(X_train, y_train)

print('Best Parameters using grid search: \n', gs.best_params_)
