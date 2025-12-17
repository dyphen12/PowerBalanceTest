# plotter.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def plot_power_balance(values, title="Power Balance Test — F-150 5.4L 3V"):
    cylinders = range(1, 9)
    
    plt.figure(figsize=(10, 4))
    plt.plot(cylinders, values, marker='o', linewidth=2)
    plt.axhline(0, linestyle='--', linewidth=1, color='gray')

    # Resalta cilindro más débil
    min_cyl_index = np.argmin(values)
    plt.plot(cylinders[min_cyl_index], values[min_cyl_index], 'ro', markersize=10, label='Cilindro problemático')

    plt.xticks(cylinders)
    plt.yticks(range(-60, 41, 20))
    plt.ylim(-65, 45)

    plt.xlabel("Cilindro")
    plt.ylabel("Índice de contribución")
    plt.title(title)
    plt.grid(True, linestyle=':', linewidth=0.7)
    plt.legend()
    plt.show()


def animate_power_balance(simulate_func, weak_cyl=None, misfire_cyl=None, frames=50, interval=300):
    cylinders = range(1, 9)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    values = simulate_func(weak_cyl, misfire_cyl)
    line, = ax.plot(cylinders, values, marker='o', linewidth=2)
    
    weak_marker, = ax.plot([], [], 'ro', markersize=10)

    ax.axhline(0, linestyle='--', linewidth=1, color='gray')
    ax.set_xticks(cylinders)
    ax.set_yticks(range(-60, 41, 20))
    ax.set_ylim(-65, 45)
    ax.set_xlabel("Cilindro")
    ax.set_ylabel("Índice de contribución")
    ax.set_title("Power Balance Test — F-150 5.4L 3V")
    ax.grid(True, linestyle=':', linewidth=0.7)

    def update(frame):
        values = simulate_func(weak_cyl, misfire_cyl)
        line.set_ydata(values)
        
        min_index = np.argmin(values)
        weak_marker.set_data([cylinders[min_index]], [values[min_index]])  # ✅ arreglado
        
        return line, weak_marker

    anim = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
    plt.show()

