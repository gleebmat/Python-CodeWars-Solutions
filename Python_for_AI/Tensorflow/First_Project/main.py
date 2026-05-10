import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input, Dropout
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


mnist = tf.keras.datasets.mnist

mnist.load_data()


(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train, X_test = X_train / 255.0, X_test / 255.0
X_train

model = Sequential()
model.add(Input((28, 28)))
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dense(128, activation="relu"))

model.add(Dense(64, activation="relu"))

model.add(Dropout(0.4))
model.add(Dense(10))

nonsense_prediction = model(X_train[:1]).numpy()
nonsense_prediction
tf.nn.softmax(nonsense_prediction).numpy()

loss_fn = SparseCategoricalCrossentropy(from_logits=True)

loss_fn(y_train[:1], nonsense_prediction)

optimizer = Adam(learning_rate=0.007)

model.compile(optimizer=optimizer, loss=loss_fn, metrics=["accuracy"])
model.fit(X_train, y_train, epochs=25)
model.evaluate(X_test, y_test)

tf.argmax(tf.nn.softmax(model(X_test[:1])).numpy(), axis=1)


# Regression -------------

scaler = StandardScaler()
df = pd.read_csv("housing.csv")

X, y = df.drop("MedHouseVal", axis=1), df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = Sequential()
model.add(Input((8,)))
model.add(Dense(256, activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mse", metrics=["mae", "r2_score"])
model.fit(X_train_scaled, y_train, epochs=15)
model.evaluate(X_test_scaled, y_test)
df.MedHouseVal.describe()
