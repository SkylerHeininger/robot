import numpy as np
import matplotlib.pyplot as plt

matrix_a = np.loadtxt("A.csv", delimiter=",")
matrix_b = np.loadtxt("B.csv", delimiter=",")

row_averages_a = np.mean(matrix_a, axis=1)
std_a = np.std(matrix_a, axis=1)

row_averages_b = np.mean(matrix_b, axis=1)
std_b = np.std(matrix_b, axis=1)

x = np.arange(matrix_a.shape[0])

plt.plot(x, row_averages_a, label='Mean', color='blue')
plt.fill_between(x, row_averages_a - std_a, row_averages_a + std_a, color='blue', alpha=0.3, label='±1 Std Dev')

plt.plot(x, row_averages_b, label='Mean', color='red', alpha=0.5)
plt.fill_between(x, row_averages_b - std_b, row_averages_b + std_b, color='red', alpha=0.2, label='±1 Std Dev')


plt.xlabel('Generation')
plt.ylabel('X position')
plt.title('Preliminary A/B Testing')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
