import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pathBoat = "data\\front_boat_data.xlsx"
rawDataBoatEx = pd.read_excel(pathBoat)
exBoatData = rawDataBoatEx.as_matrix()

time = rawDataBoatEx["Time"].tolist()
x = rawDataBoatEx["X"].tolist()
y = rawDataBoatEx["Y"].tolist()
z = rawDataBoatEx["Z"].tolist()

fig = plt.figure()

plt.title("Z-coordinate of front pivot point")
plt.grid(True)
plt.xlabel("Timeframe")
plt.ylabel("Z - coord")
# ax = fig.add_subplot(111, projection='3d')
# ax.axis('equal')
# ax.scatter(x, y, z, c=time)
Xlin = np.arange(0, len(z), 1)
plt.plot(Xlin, z, '-ro')
plt.show()

######################################################

# pathWater = "data\\water_data.xlsx"
pathWater = "data\\waterNew.xlsx"
rawDataWaterEx = pd.read_excel(pathWater)
rawDataWaterEx = rawDataWaterEx[rawDataWaterEx['Density(rho)'] != 1000.0]
exWaterData = rawDataWaterEx.as_matrix()

print(rawDataWaterEx)

x = rawDataWaterEx["X"].tolist()
y = rawDataWaterEx["Y"].tolist()
z = rawDataWaterEx["Z"].tolist()
rho = rawDataWaterEx["Density(rho)"].tolist()

fig = plt.figure()
plt.title("Water particles")
ax = fig.add_subplot(111, projection='3d')
ax.axis('equal')
ax.scatter(x, y, z, c=rho)
plt.show()

###############################
rawDataWaterEx.sort_values(by=['Z'])
rawDataWaterEx = rawDataWaterEx.drop_duplicates(['X', 'Y'], keep='last')
print(rawDataWaterEx)

x = rawDataWaterEx["X"].tolist()
y = rawDataWaterEx["Y"].tolist()
z = rawDataWaterEx["Z"].tolist()
rho = rawDataWaterEx["Density(rho)"].tolist()

fig = plt.figure()
plt.title("Sliced water particles")
ax = fig.add_subplot(111, projection='3d')
ax.axis('equal')
ax.scatter(x, y, z, c=(rho))
plt.show()
