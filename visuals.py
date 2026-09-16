import numpy as np
import matplotlib.pyplot as plt
from rotations import orbital_rotation

def plot_ellipse(planet, color='black'):
    inclination = planet["inclination"]
    longitude_of_ascending_node = planet["longitude_of_ascending_node"]
    argument_of_periapsis = planet["argument_of_periapsis"]
    focal_distance=planet["focal_distance"]
    semi_major_axis=planet["semi_major_axis"]
    semi_minor_axis=planet["semi_minor_axis"]
    
    theta = np.linspace(0, 2 * np.pi, 1000)

    # Эллипс в собственной плоскости орбиты
    x_orb = focal_distance + semi_major_axis * np.cos(theta)
    y_orb = semi_minor_axis * np.sin(theta)
    z_orb = np.zeros_like(theta)

    points = np.vstack((x_orb, y_orb, z_orb))

    # Поворот орбиты
    R = orbital_rotation(
        longitude_of_ascending_node,
        inclination,
        argument_of_periapsis
    )

    points_rotated = R @ points

    # Проекция на XY
    x = points_rotated[0]
    y = points_rotated[1]

    plt.plot(x, y, color=color)

def dot(planet):
    inclination = planet["inclination"]
    longitude_of_ascending_node = planet["longitude_of_ascending_node"]
    argument_of_periapsis = planet["argument_of_periapsis"]
    focal_distance=planet["focal_distance"]
    semi_major_axis=planet["semi_major_axis"]
    semi_minor_axis=planet["semi_minor_axis"]
    eccentric_anomaly=planet["eccentric_anomaly"]

    R = orbital_rotation(
        longitude_of_ascending_node,
        inclination,
        argument_of_periapsis
    )

    point=np.array([
        semi_major_axis * np.cos(eccentric_anomaly) + focal_distance,
        semi_minor_axis * np.sin(eccentric_anomaly),
        0
        ])
    point_rotated = R @ point
    x = point_rotated[0]
    y = point_rotated[1]
    plt.plot(x, y, 'o')   
