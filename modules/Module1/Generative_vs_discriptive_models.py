import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

# Generate some synthetic data
np.random.seed(0)
class0 = np.random.multivariate_normal([2, 2], [[1, 0.75], [0.75, 1]], 100)
class1 = np.random.multivariate_normal([6, 6], [[1, 0.75], [0.75, 1]], 100)

# Create a plot
plt.figure(figsize=(10, 5))

# Discriminative model subplot
plt.subplot(1, 2, 1)
plt.scatter(class0[:, 0], class0[:, 1], color='skyblue', label='Class 0')
plt.scatter(class1[:, 0], class1[:, 1], color='salmon', label='Class 1')
plt.plot([0, 8], [0, 8], 'k--', label='Decision Boundary')
plt.title('Discriminative Model')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)

# Generative model subplot
plt.subplot(1, 2, 2)
plt.scatter(class0[:, 0], class0[:, 1], color='skyblue', label='Class 0')
plt.scatter(class1[:, 0], class1[:, 1], color='salmon', label='Class 1')

def draw_ellipse(position, covariance, ax, color):
    covariance = np.array(covariance)  # Convert to NumPy array
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(xy=position, width=nsig*width, height=nsig*height,
                             angle=angle, edgecolor=color, facecolor='none', linestyle='--'))
    

ax = plt.gca()
draw_ellipse([2, 2], [[1, 0.75], [0.75, 1]], ax, 'blue')
draw_ellipse([6, 6], [[1, 0.75], [0.75, 1]], ax, 'red')

plt.title('Generative Model')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
