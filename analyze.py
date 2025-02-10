import matplotlib.pyplot as plt
import numpy as np

data_back = np.load("data/backLegSensor.npy")
data_front = np.load("data/frontLegSensor.npy")


plt.plot(data_back, linewidth=3, label="Back Leg")
plt.plot(data_front, label="Front Leg")
plt.legend()
plt.show()
