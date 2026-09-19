#Imports
import requests
API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

from calculations import orbital_rotation, angle, angle_find
from visuals import plot_ellipse, dot, custom_dot


def jd_to_datetime(julian_date): #Transfer julian date to normal date standart
    unix_epoch = 2440587.5
    seconds = (julian_date - unix_epoch) * 86400

    return datetime(1970, 1, 1) + timedelta(seconds=seconds)

#Getting an actual constants

def get_ephemeris(body_id, date=None):

    
    if date is None:
        date = datetime.now(timezone.utc)

    elif isinstance(date, str):
        date = datetime.fromisoformat(date)

    stop_date = date + timedelta(days=1)

    params = {
        "format": "json",

        "COMMAND": f"'{body_id}'",
        "OBJ_DATA": "NO",

        # Солнце как центр координат
        "CENTER": "'500@10'",

        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "ELEMENTS",

        "START_TIME": f"'{date.strftime('%Y-%m-%d %H:%M')}'",
        "STOP_TIME": f"'{stop_date.strftime('%Y-%m-%d %H:%M')}'",
        "STEP_SIZE": "'1 d'",

        "REF_PLANE": "ECLIPTIC",
        "REF_SYSTEM": "J2000",
        "OUT_UNITS": "KM-S",

        "CSV_FORMAT": "YES",
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])
    text = data["result"]
    data_section = text.split("$$SOE")[1].split("$$EOE")[0].strip()
    line = data_section.splitlines()[0]
    values = [x.strip() for x in line.split(",")]
    return {
    "epoch": float(values[0]),
    "date": values[1],

    # Orbital Elements
    "eccentricity": float(values[2]),
    "periapsis_distance": float(values[3]),

    # Angles -> radians
    "inclination": np.radians(float(values[4])),
    "longitude_of_ascending_node": np.radians(float(values[5])),
    "argument_of_periapsis": np.radians(float(values[6])),
    "periapsis_time": float(values[7]),
    "mean_motion": np.radians(float(values[8])),
    "mean_anomaly": np.radians(float(values[9])),
    "true_anomaly": np.radians(float(values[10])),

    "semi_major_axis": float(values[11]),
    "apoapsis_distance": float(values[12]),
    "period": float(values[13]),
}


def derivative_parameters(planet):
    semi_major_axis = planet["semi_major_axis"]
    eccentricity = planet["eccentricity"]
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)
    focal_distance = semi_major_axis * eccentricity

    eccentricity=planet["eccentricity"]
    mean_anomaly=planet["mean_anomaly"]
    eccentric_anomaly=mean_anomaly
    for i in range(0,5):
            eccentric_anomaly=eccentric_anomaly-((eccentric_anomaly-mean_anomaly-eccentricity*np.sin(eccentric_anomaly))/(1-eccentricity*np.cos(eccentric_anomaly)))

    planet["eccentric_anomaly"]=float(eccentric_anomaly)
    planet["semi_minor_axis"]=float(semi_minor_axis)
    planet["focal_distance"]=float(focal_distance)
    
    
plt.plot(0, 0, 'o', color='red', markersize=10, label='Sun')

earth=get_ephemeris(399)
mars=get_ephemeris(499)
derivative_parameters(earth)
derivative_parameters(mars)

plot_ellipse(mars)
plot_ellipse(earth)
dot(mars, "orange")
dot(earth, "blue")
custom_dot(earth["semi_major_axis"],earth["semi_minor_axis"],earth["focal_distance"],earth["longitude_of_ascending_node"],earth["inclination"],earth["argument_of_periapsis"],0,"pink")
custom_dot(earth["semi_major_axis"],earth["semi_minor_axis"],earth["focal_distance"],earth["longitude_of_ascending_node"],earth["inclination"],earth["argument_of_periapsis"],np.pi)
custom_dot(mars["semi_major_axis"],mars["semi_minor_axis"],mars["focal_distance"],mars["longitude_of_ascending_node"],mars["inclination"],mars["argument_of_periapsis"],0,"pink")
custom_dot(mars["semi_major_axis"],mars["semi_minor_axis"],mars["focal_distance"],mars["longitude_of_ascending_node"],mars["inclination"],mars["argument_of_periapsis"],np.pi)
#print(earth["longitude_of_ascending_node"])
#q=(angle(earth, mars))
#print(earth["true_anomaly"])
#print(mars["true_anomaly"])
#print(q)
#print(mars["true_anomaly"]+earth["true_anomaly"]-np.degrees(q))
angle_find(earth,mars)
plt.title("Mars and Earth orbital locations")
plt.axis("equal")
plt.grid()
plt.show()
