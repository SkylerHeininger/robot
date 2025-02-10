import matplotlib.pyplot as plt
import numpy as np
import math

# data_back = np.load("data/backLegSensor.npy")
# data_front = np.load("data/frontLegSensor.npy")
#
#
# plt.plot(data_back, linewidth=3, label="Back Leg")
# plt.plot(data_front, label="Front Leg")
# plt.legend()
# plt.show()


# data_angles = np.load("data/manualAngles.npy")
front_angles = np.load("data/frontAngles.npy")
back_angles = np.load("data/backAngles.npy")


import matplotlib.pylab as plt
x = np.linspace(-np.pi, np.pi, 1000)
plt.plot(x, front_angles, linewidth=3, label="Front leg motor values")
plt.plot(x, back_angles, linewidth=0.5, label="Back leg motor values")
plt.legend()
plt.show()

