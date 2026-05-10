from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

param_grid = {
    "n_estimators": [100, 200, 300],
    "min_samples_split": [2, 4],
    "max_depth": [None, 4, 8],
}
scaler = StandardScaler()
forest = RandomForestRegressor()
grid_search = GridSearchCV(
    forest, param_grid, cv=5, scoring="neg_mean_squared_error", return_train_score=True
)

data = pd.read_csv("housing.csv")
data.info()
data.dropna(inplace=True)
data.info()


X = data.drop(["median_house_value"], axis=1)
y = data["median_house_value"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train
X_test
y_train
y_test

train_data = X_train.join(y_train)
train_data.hist(figsize=(15, 8))
plt.figure(figsize=(15, 8))
sns.heatmap(train_data.corr(numeric_only=True), annot=True, cmap="YlGnBu")

train_data["total_rooms"] = np.log(train_data["total_rooms"] + 1)
train_data["total_bedrooms"] = np.log(train_data["total_bedrooms"] + 1)
train_data["population"] = np.log(train_data["population"] + 1)
train_data["households"] = np.log(train_data["households"] + 1)

train_data.hist(figsize=(15, 8))

train_data.ocean_proximity.value_counts()
train_data = train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(
    ["ocean_proximity"], axis=1
)

plt.figure(figsize=(15, 8))
sns.heatmap(train_data.corr(), annot=True, cmap="YlGnBu")
plt.figure(figsize=(15, 8))
sns.scatterplot(
    x="latitude",
    y="longitude",
    data=train_data,
    hue="median_house_value",
    palette="coolwarm",
)
train_data["bedroom_ratio"] = train_data["total_bedrooms"] / train_data["total_rooms"]

train_data["household_rooms"] = train_data["total_rooms"] / train_data["households"]

sns.heatmap(train_data.corr(), annot=True, cmap="YlGnBu")

X_train, y_train = (
    train_data.drop(["median_house_value"], axis=1),
    train_data["median_house_value"],
)
X_train_s = scaler.fit_transform(X_train)
reg = LinearRegression()

reg.fit(X_train_s, y_train)

test_data = X_test.join(y_test)

test_data["total_rooms"] = np.log(test_data["total_rooms"] + 1)
test_data["total_bedrooms"] = np.log(test_data["total_bedrooms"] + 1)
test_data["population"] = np.log(test_data["population"] + 1)
test_data["households"] = np.log(test_data["households"] + 1)

test_data = test_data.join(pd.get_dummies(test_data.ocean_proximity)).drop(
    ["ocean_proximity"], axis=1
)

test_data["bedroom_ratio"] = test_data["total_bedrooms"] / test_data["total_rooms"]
test_data["household_rooms"] = test_data["total_rooms"] / test_data["households"]
X_test, y_test = (
    test_data.drop(["median_house_value"], axis=1),
    test_data["median_house_value"],
)

X_test_s = scaler.transform(X_test)
forest.fit(X_train_s, y_train)
forest.score(X_test_s, y_test)
reg.score(X_test_s, y_test)
grid_search.fit(X_train_s, y_train)
best_estimator = grid_search.best_estimator_
best_estimator.score(X_test_s, y_test)
