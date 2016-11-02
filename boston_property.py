import numpy as np
import pandas as pd
import visuals as vs # Supplementary code
import sklearn
from sklearn.cross_validation import ShuffleSplit
from sklearn import cross_validation
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.grid_search import GridSearchCV
# Pretty display for notebooks
#%matplotlib inline
import matplotlib


def performance_metric(y_true, y_predict):
    """ Calculates and returns the performance score between
        true and predicted values based on the metric chosen. """

    # TODO: Calculate the performance score between 'y_true' and 'y_predict'
    score = sklearn.metrics.r2_score(y_true, y_predict)

    # Return the score
    return score

def fit_model2(X,y):
    cv_sets = ShuffleSplit(X.shape[0], n_iter=10, test_size=0.20, random_state=0)
    regressor = DecisionTreeRegressor()
    regressor.fit(X, y)
    params = {'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}

    scoring_fnc = make_scorer(mean_squared_error)
    grid_obj = GridSearchCV(regressor, params, scoring=scoring_fnc, cv=cv_sets)
    grid = grid_obj.fit(X, y)
    return grid.best_estimator_


def fit_model1(X, y):
    """ Performs grid search over the 'max_depth' parameter for a
        decision tree regressor trained on the input data [X, y]. """

    # Create cross-validation sets from the training data
    cv_sets = ShuffleSplit(X.shape[0], n_iter=10, test_size=0.20, random_state=0)

    # TODO: Create a decision tree regressor object
    regressor = DecisionTreeRegressor()
    regressor.fit(X, y)
    # TODO: Create a dictionary for the parameter 'max_depth' with a range from 1 to 10
    params = {'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}

    # TODO: Transform 'performance_metric' into a scoring function using 'make_scorer'
    scoring_fnc = make_scorer(performance_metric)

    #print(regressor.predict(X))
    ##scoring_fnc = make_scorer(mean_squared_error)

    # TODO: Create the grid search object
    grid_obj = GridSearchCV(regressor, params, scoring=scoring_fnc, cv=cv_sets)

    # Fit the grid search object to the data to compute the optimal model
    grid = grid_obj.fit(X, y)

    # Return the optimal model after fitting the data
    return grid.best_estimator_




# Load the Boston housing dataset
data = pd.read_csv('housing.csv')
prices = data['MEDV']
features = data.drop('MEDV', axis = 1)

# Success
print ("Boston housing dataset has {} data points with {} variables each.".format(*data.shape))
#print(features)

if False:
    # TODO: Minimum price of the data
    minimum_price = np.min(prices)

    # TODO: Maximum price of the data
    maximum_price = np.max(prices)

    # TODO: Mean price of the data
    mean_price = np.mean(prices)

    # TODO: Median price of the data
    median_price = np.median(prices)

    # TODO: Standard deviation of prices of the data
    std_price = np.std(prices)

    # Show the calculated statistics
    print("Statistics for Boston housing dataset:\n")
    print("Minimum price: ${:,.2f}".format(minimum_price))
    print("Maximum price: ${:,.2f}".format(maximum_price))
    print("Mean price: ${:,.2f}".format(mean_price))
    print("Median price ${:,.2f}".format(median_price))
    print("Standard deviation of prices: ${:,.2f}".format(std_price))

if False:
    score = performance_metric([3, -0.5, 2, 7, 4.2], [2.5, 0.0, 2.1, 7.8, 5.3])
    print("Model has a coefficient of determination, R^2, of {:.3f}.".format(score))

X_train, X_test, y_train, y_test = cross_validation.train_test_split(features,prices,test_size=0.2, random_state=0)
#vs.ModelComplexity(X_train, y_train)

#reg = fit_model1(X_train, y_train)
#print(reg.get_params()['max_depth'])

client_data = [[5, 17, 15], # Client 1
               [4, 32, 22], # Client 2
               [8, 3, 12]]
regressor = DecisionTreeRegressor(max_depth=4)
regressor.fit(X_train, y_train)
result = regressor.predict(client_data)




client_data = [[5, 17, 15], # Client 1
               [4, 32, 22], # Client 2
               [8, 3, 12]]  # Client 3

reg = DecisionTreeRegressor(max_depth=4)
reg.fit(features,prices)
#result = reg.predict(client_data)

# Show predictions
for i, price in enumerate(reg.predict(client_data)):
    print("Predicted selling price for Client {}'s home: ${:,.2f}".format(i+1, price))
print(result)
exit(0)