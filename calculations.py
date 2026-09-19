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

def angle(planet1,planet2):

    R_1 = orbital_rotation(
            planet1["longitude_of_ascending_node"],
            planet1["inclination"],
            planet1["argument_of_periapsis"]
        )
    
    point1=np.array([
        planet1["periapsis_distance"],
        0,
        0
        ])
    point_rotated_1 = R_1 @ point1
    x_1 = point_rotated_1[0]
    y_1 = point_rotated_1[1]
    z_1 = point_rotated_1[2]

    R_2 = orbital_rotation(
                planet2["longitude_of_ascending_node"],
                planet2["inclination"],
                planet2["argument_of_periapsis"]
            )
        
    point2=np.array([
        planet2["periapsis_distance"],
        0,
        0
        ])
    point_rotated_2 = R_2 @ point2
    x_2 = point_rotated_2[0]
    y_2 = point_rotated_2[1]
    z_2 = point_rotated_2[2]


    ang=np.arccos((x_1*x_2+y_1*y_2+z_1*z_2)/(np.sqrt((x_1**2)+(y_1**2)+(z_1**2))*np.sqrt((x_2**2)+(y_2**2)+(z_2**2))))
    return ang

def angle_find(planet1,planet2): #Доработать
    day=0
    periapsis_angle=angle(planet1,planet2)
    true_anomaly_1=planet1["true_anomaly"]
    true_anomaly_2=planet2["true_anomaly"]
    mean_anomaly_1=planet1["mean_anomaly"]
    mean_anomaly_2=planet2["mean_anomaly"]
    