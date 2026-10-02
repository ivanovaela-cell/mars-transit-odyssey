# -*- coding: utf-8 -*-
"""
Симуляция гомановского перелёта Земля - Марс (Python + Matplotlib)
На основе математической модели из ODT-документа.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Константы (Астрономические единицы AU и годы)
a_earth = 1.0       # AU
a_mars = 1.524      # AU
a_transfer = (a_earth + a_mars) / 2.0  # 1.262 AU
e_transfer = 1.0 - a_earth / a_transfer # ~0.208
T_transfer = a_transfer ** 1.5         # ~1.417 года
t_transfer = T_transfer / 2.0          # ~0.7085 года (~258.7 дней)

omega_earth = 2.0 * np.pi / 1.0        # рад/год
omega_mars = 2.0 * np.pi / 1.88        # рад/год

# Фазовый угол Марса в момент запуска (для точной встречи)
phi = np.pi - omega_mars * t_transfer  # ~44.3 градуса

# Временная шкала
dt = 0.005 # шаг времени в годах (~1.8 дня)
t_max = t_transfer
t_arr = np.arange(0, t_max + dt, dt)

def solve_kepler(M, e, tol=1e-6, max_iter=100):
    """Численное решение уравнения Кеплера M = E - e*sin(E) методом Ньютона"""
    E = M
    for _ in range(max_iter):
        E_next = M + e * np.sin(E)
        if np.abs(E_next - E) < tol:
            return E_next
        E = E_next
    return E

def position_earth(t):
    theta = omega_earth * t
    return a_earth * np.cos(theta), a_earth * np.sin(theta), 0.0

def position_mars(t):
    theta = phi + omega_mars * t
    return a_mars * np.cos(theta), a_mars * np.sin(theta), 0.0

def position_rocket(t):
    if t >= t_transfer:
        return position_mars(t_transfer)
    M = np.pi * (t / t_transfer)
    E = solve_kepler(M, e_transfer)
    x = a_transfer * (np.cos(E) - e_transfer)
    y = a_transfer * np.sqrt(1.0 - e_transfer**2) * np.sin(E)
    return x, y, 0.0

# Настройка 3D графика
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('#050811')
ax.set_facecolor('#050811')

ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-1.7, 1.7)
ax.set_zlim(-0.5, 0.5)

ax.set_xlabel('X (AU)', color='white')
ax.set_ylabel('Y (AU)', color='white')
ax.set_zlabel('Z (AU)', color='white')
ax.tick_params(colors='white')
ax.set_title('Гомановский перелет Земля - Марс (Matplotlib 3D)', color='cyan', fontsize=14, pad=15)

# Сетка
ax.xaxis._axinfo["grid"]['color'] = (0.2, 0.3, 0.4, 0.3)
ax.yaxis._axinfo["grid"]['color'] = (0.2, 0.3, 0.4, 0.3)
ax.zaxis._axinfo["grid"]['color'] = (0.2, 0.3, 0.4, 0.3)

# Солнце
ax.scatter([0], [0], [0], color='#ffaa00', s=250, label='Солнце', edgecolors='yellow')

# Орбита Земли
theta_orbit = np.linspace(0, 2 * np.pi, 200)
ax.plot(a_earth * np.cos(theta_orbit), a_earth * np.sin(theta_orbit), np.zeros_like(theta_orbit),
        color='#00d2ff', linestyle='--', linewidth=1.2, label='Орбита Земли (1.00 AU)')

# Орбита Марса
ax.plot(a_mars * np.cos(theta_orbit), a_mars * np.sin(theta_orbit), np.zeros_like(theta_orbit),
        color='#ff5733', linestyle='--', linewidth=1.2, label='Орбита Марса (1.52 AU)')

# Траектория перелета
M_transfer = np.linspace(0, np.pi, 150)
E_transfer = [solve_kepler(m, e_transfer) for m in M_transfer]
x_trans = [a_transfer * (np.cos(e) - e_transfer) for e in E_transfer]
y_trans = [a_transfer * np.sqrt(1.0 - e_transfer**2) * np.sin(e) for e in E_transfer]
ax.plot(x_trans, y_trans, np.zeros_like(x_trans), color='#ffd700', linewidth=1.8, label='Гомановская траектория')

# Точки планет и ракеты
earth_point, = ax.plot([], [], [], 'o', color='#00d2ff', markersize=9, label='Земля')
mars_point, = ax.plot([], [], [], 'o', color='#ff5733', markersize=8, label='Марс')
rocket_point, = ax.plot([], [], [], '^', color='#ffffff', markersize=8, label='Корабль')

# Траектория полета ракеты (хвост)
trail_line, = ax.plot([], [], [], color='white', linestyle=':', linewidth=1.0, alpha=0.7)
rocket_x_hist, rocket_y_hist = [], []

time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, color='cyan', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a1224', alpha=0.8, edgecolor='#00d2ff'))

def update(frame):
    t = t_arr[frame]
    xe, ye, ze = position_earth(t)
    xm, ym, zm = position_mars(t)
    xr, yr, zr = position_rocket(t)

    earth_point.set_data([xe], [ye])
    earth_point.set_3d_properties([ze])

    mars_point.set_data([xm], [ym])
    mars_point.set_3d_properties([zm])

    rocket_point.set_data([xr], [yr])
    rocket_point.set_3d_properties([zr])

    rocket_x_hist.append(xr)
    rocket_y_hist.append(yr)
    trail_line.set_data(rocket_x_hist, rocket_y_hist)
    trail_line.set_3d_properties(np.zeros(len(rocket_x_hist)))

    day = t * 365.25
    dist_mars = np.sqrt((xr - xm)**2 + (yr - ym)**2) * 149.6
    time_text.set_text(f'Время: {day:.1f} / {t_transfer*365.25:.1f} дней\nДистанция до Марса: {dist_mars:.1f} млн км')

    return earth_point, mars_point, rocket_point, trail_line, time_text

ani = FuncAnimation(fig, update, frames=len(t_arr), interval=35, blit=False, repeat=True)
ax.legend(loc='lower left', facecolor='#0a1224', edgecolor='#00d2ff', labelcolor='white')

if __name__ == '__main__':
    plt.show()
