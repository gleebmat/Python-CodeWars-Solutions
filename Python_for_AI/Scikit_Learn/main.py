from sklearn.datasets import load_breast_cancer, fetch_california_housing, load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)

# print(knn.score(X_test_scaled,y_test))
data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
positions = np.arange(3)
counts = np.bincount(y_test)
plt.bar(positions, counts)
plt.xticks(positions, data.target_names)
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2)
for train_idx, test_idx in split.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

X, y = load_iris(return_X_y=True)

scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train_scaled = scaler.fit_transform(X_train)
X_train_scaled


(X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import OrdinalEncoder

data = fetch_openml("car", as_frame=True).frame

columns_to_encode = ["lug_boot", "safety"]
encoder = OrdinalEncoder(categories=[["small", "med", "big"], ["low", "med", "high"]])
data[columns_to_encode] = encoder.fit_transform(data[columns_to_encode])

data = fetch_openml("adult", as_frame=True).frame
from sklearn.preprocessing import OneHotEncoder

data.occupation.value_counts()
import pandas as pd

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

encoded_values = encoder.fit_transform(data[["occupation", "race"]])
new_cols = encoder.get_feature_names_out(["occupation", "race"])
df_encoded = pd.DataFrame(encoded_values, columns=new_cols, index=data.index)
data_final = pd.concat([data.drop(columns=["occupation", "race"]), df_encoded])
data_final
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)


X_test_scaled = scaler.transform(X_test)
clf = LogisticRegression()

clf.fit(X_train_scaled, y_train)
clf.score(X_test_scaled, y_test)
single_instance = X_test_scaled[0]
single_instance
clf.predict([single_instance])
y_test[0]
clf.predict_proba([single_instance])

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

reg = LinearRegression()
reg.fit(X_train_scaled, y_train)
reg.score(X_test_scaled, y_test)


single = X_test_scaled[0]
reg.predict([single])
X, _ = make_moons(n_samples=10000, noise=0.05)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


k_means = KMeans(n_clusters=5)
k_means.fit(X_scaled)
plt.scatter(X_scaled[:, 0], X_scaled[:, 1])

X, y = fetch_openml("mnist_784", return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


pca = PCA(n_components=10)
X_train_reduced = pca.fit_transform(X_train)
X_test_reduced = pca.transform(X_test)
clf = LogisticRegression(max_iter=100)
clf.fit(X_train_reduced, y_train)

print(clf.score(X_test_reduced, y_test))

pca.explained_variance_ratio_

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)
clf = KNeighborsClassifier()
clf.fit(X_train_scaled, y_train)

clf.score(X_test_scaled, y_test)  # Accuracy

y_pred = clf.predict(X_test_scaled)
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred)
recall_score(y_test, y_pred)
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

pipe = Pipeline(
    [
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=10)),
        ("forest", RandomForestClassifier()),
    ]
)

pipe.fit(X_train, y_train)

pipe.score(X_test, y_test)
