import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# входные параметры 
periods = 5
fps_save = 30

# рассчитываем параметры 
x_data = np.arange(0, periods * 2 * np.pi, 0.01)
y_data = np.sin(x_data)
quantity_frame = np.arange(0, periods * 2 * np.pi, 0.2)

# рисуем график 
fig, ax = plt.subplots()
line = plt.plot(x_data, y_data)
ax.set_title(f'Animated sunus graph {periods} period')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# делаем точку которая будет бегать по графику 
ax = plt.axis([0, periods * 2 * np.pi, -1.2, 1.2])
dot, = plt.plot([0], [np.sin(0)], 'ro')
   
# анимируем точку и показываем график 
animation = FuncAnimation(fig, lambda i: dot.set_data(i, np.sin(i)), frames=quantity_frame, interval=10)
animation.save(f'Animated sunus graph {periods} period.gif', writer=PillowWriter(fps=fps_save))
plt.show()