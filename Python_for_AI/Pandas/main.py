import pandas as pd
from sklearn.datasets import fetch_california_housing
import matplotlib.pyplot as plt
import yfinance as yf

stock_df = yf.download("AAPL")

values = [10, 20, 30, 40, 50]
s = pd.Series(values, index=["a", "b", "c", "d", "e"])

s.loc["a"]


# Data Frame
df = pd.DataFrame(
    {
        "name": ["Gleb", "Alice", "Victor"],
        "age": [30, 40, 50],
        "job": ["proger", "footballer", "designer"],
    }
)

df = df.set_index("name")
df.loc["Gleb"]
df1 = pd.DataFrame({"a": [1, 2, 3]}, index=[0, 1, 2])
df2 = pd.DataFrame({"a": [10, 20, 30]}, index=[2, 0, 1])
df1 * df2

df = df.reset_index()
df.to_csv("mydata.csv")
pd.read_csv("mydata.csv", index_col=0)

df = fetch_california_housing(as_frame=True).frame
df = pd.DataFrame(
    {
        "name": ["mike", "alice", "bob"],
        "age": [30, 40, 50],
        "job": ["prog", "foot", "acc"],
    }
)
df.loc[1]
df.sample()
list(df.columns)
df.describe()
df.HouseAge.hist()
plt.title("111")
plt.tight_layout()
df.hist()
df1 = pd.DataFrame({"Item": ["A", "B", "C"], "Price": [10, 20, 30]})
df2 = pd.DataFrame({"Item": ["D", "E", "F"], "Price": [40, 50, 60]})
pd.concat([df1, df2]).reset_index().drop("index", axis=1)

pd.concat([df1, df2], axis=1)
df3 = pd.DataFrame({"Item": ["B", "C", "D"], "Country": ["X", "Y", "Z"]})

pd.merge(df1, df3, how="outer")
