import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

import random

style.use("ggplot")
# years=[2006+x for x in range(16)]
# print(years)
# weights=[80,83,84,85,86,82,81,79,83,80,
#          82,82,83,81,80,79]

# print(len(years))
# print(len(weights))
# plt.plot(years,weights,"r--",lw=2)

# x=["C++","C#","Pyhton","Java","Go"]
# y=np.array([20,50,140,1,45])
# y*=3
# plt.bar(x,y,color="r",align="center",width=0.5,edgecolor="black",lw=10)

# ages=np.random.normal(20,1.5,1000)
# plt.hist(ages,bins=[ages.min(),18,21,ages.max()],cumulative=True)

# heights=np.random.normal(160,79,30)
# plt.boxplot(heights)
# first=np.linspace(0,10,25)
# second=np.linspace(10,200,25)
# data=np.concatenate((first,second))
# plt.boxplot(data)


# years=[2022,2023,2024,2025,2026]
# income=[10,14,16,17,11]
# plt.plot(years,income)
# plt.title("Happiness of Gleb",fontsize=30)
# plt.xlabel("Year")
# plt.ylabel("identities")
# plt.yticks([5,6,7,8,9,10,11,12,13,14,15,16,17,18],)

# ax = plt.axes(projection="3d")
# x = np.random.random(100)
# y = np.random.random(100)
# z = np.random.random(100)


# ax.scatter(x, y, z)
# ax.set_title("3D")
# plt.show()


heads_tails = [0, 0]
for _ in range(100000):
    heads_tails[random.randint(0, 1)] += 1
    plt.bar(["Heads", "Tails"], heads_tails, color=["red", "blue"])
    plt.pause(0.001)

plt.show()
