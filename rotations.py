import numpy as np 

#Rotational matrixes
def Rz(angle):
    angle = np.radians(angle)

    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1]
    ])


def Rx(angle):
    angle = np.radians(angle)

    return np.array([
        [1, 0,              0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle),  np.cos(angle)]
    ])


def orbital_rotation(Omega, i, omega):
    return Rz(Omega) @ Rx(i) @ Rz(omega)