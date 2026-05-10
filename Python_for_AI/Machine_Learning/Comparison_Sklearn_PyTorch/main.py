import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

scaler = StandardScaler()
forest = RandomForestRegressor
data = pd.read_csv("housing.csv")
X = data.drop(["median_house_value"], axis=1)
y = data["median_house_value"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

train_data = X_train.join(y_train)
train_data
train_data.hist(figsize=(20, 10))
sns.heatmap(train_data.corr(numeric_only=True), annot=True, cmap="YlGnBu")


train_data["total_rooms"] = np.log(train_data["total_rooms"] + 1)
train_data["total_bedrooms"] = np.log(train_data["total_bedrooms"] + 1)
train_data["population"] = np.log(train_data["population"] + 1)
train_data["households"] = np.log(train_data["households"] + 1)

train_data = train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(
    ["ocean_proximity"], axis=1
)

train_data["bedroom_ratio"] = train_data["total_bedrooms"] / train_data[
    "total_rooms"
].replace(0, np.nan)
train_data["bedroom_ratio"] = train_data["bedroom_ratio"].fillna(0)
train_data["household_rooms"] = train_data["total_rooms"] / train_data["households"]


reg = LinearRegression()


test_data = X_test.join(y_test)


test_data["total_rooms"] = np.log(test_data["total_rooms"] + 1)
test_data["total_bedrooms"] = np.log(test_data["total_bedrooms"] + 1)
test_data["population"] = np.log(test_data["population"] + 1)
test_data["households"] = np.log(test_data["households"] + 1)

test_data = test_data.join(pd.get_dummies(test_data.ocean_proximity)).drop(
    ["ocean_proximity"], axis=1
)
test_data["bedroom_ratio"] = test_data["total_bedrooms"] / test_data[
    "total_rooms"
].replace(0, np.nan)
test_data["bedroom_ratio"] = test_data["bedroom_ratio"].fillna(0)
test_data["household_rooms"] = test_data["total_rooms"] / test_data["households"]

train_data, test_data = train_data.align(test_data, join="left", axis=1, fill_value=0)

X_test, y_test = (
    test_data.drop(["median_house_value"], axis=1),
    test_data["median_house_value"],
)

X_train = train_data.drop("median_house_value", axis=1)
y_train = train_data["median_house_value"]

X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_test = X_test.replace([np.inf, -np.inf], np.nan)

X_train = X_train.fillna(X_train.median())
X_test = X_test.fillna(X_test.median())
X_train_s = scaler.fit_transform(X_train)

X_test_s = scaler.transform(X_test)
reg.fit(X_train_s, y_train)
reg.score(X_test_s, y_test)
