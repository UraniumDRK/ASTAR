#Imports
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta, timezone

API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
#Solvers

def get_ephemeris(body_id, date=None):

    # Если дата не указана, берём текущую
    if date is None:
        date = datetime.now(timezone.utc)

    # Если дата передана строкой
    elif isinstance(date, str):
        date = datetime.fromisoformat(date)

    # Horizons требует, чтобы конечная дата была позже начальной
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

    # Получаем текстовый результат Horizons
    text = data["result"]

    # Берём только данные между $$SOE и $$EOE
    data_section = text.split("$$SOE")[1].split("$$EOE")[0].strip()

    # Берём первую строку
    line = data_section.splitlines()[0]

    # Разбираем CSV
    values = [x.strip() for x in line.split(",")]

    # Создаём словарь
    return {
        "epoch": float(values[0]),
        "date": values[1],

        # Орбитальные элементы
        "eccentricity": float(values[2]),                           
        "periapsis_distance": float(values[3]),
        "inclination": float(values[4]),
        "longitude_of_ascending_node": float(values[5]),
        "argument_of_periapsis": float(values[6]),
        # Время перицентра
        "periapsis_time": float(values[7]),
        "mean_motion": float(values[8]),
        "mean_anomaly": float(values[9]),
        "true_anomaly": float(values[10]),
        "semi_major_axis": float(values[11]),
        "apoapsis_distance": float(values[12]),
        "period": float(values[13]),
    }
   


def jd_to_datetime(julian_date): # Перовод из юлианской даты в обчную
    unix_epoch = 2440587.5
    seconds = (julian_date - unix_epoch) * 86400

    return datetime(1970, 1, 1) + timedelta(seconds=seconds)

#Visuals
def orbit(semi_major_axis,eccentricity):
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)
    focal_distance = semi_major_axis * eccentricity
    plot_ellipse(semi_major_axis, semi_minor_axis, focal_distance, color='black')
    
def plot_ellipse(semi_major_axis, semi_minor_axis, focal_distance ,color):
    x = np.linspace(focal_distance - semi_major_axis, focal_distance + semi_major_axis, 1000)
    y = semi_minor_axis * np.sqrt(1 - ((x - focal_distance) ** 2) / semi_major_axis**2)
    plt.plot(x, y, color=color)
    plt.plot(x, -y, color=color)

def dot(semi_major_axis,eccentricity,true_anomaly,color):
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)
    focal_distance = semi_major_axis * eccentricity
    x = semi_major_axis * np.cos(true_anomaly) + focal_distance
    y = semi_minor_axis * np.sin(true_anomaly)
    plt.plot(x, y, 'o', color=color)

plt.plot(0, 0, 'o', color='red', markersize=10, label='Sun')
mars=get_ephemeris(499,"2026-08-23")
earth=get_ephemeris(399,"2026-08-23")

orbit(mars["semi_major_axis"],mars["eccentricity"])
dot(mars["semi_major_axis"],mars["eccentricity"],mars["true_anomaly"],"sienna")

orbit(earth["semi_major_axis"],earth["eccentricity"])
dot(earth["semi_major_axis"],earth["eccentricity"],earth["true_anomaly"],"green")
plt.title("Расположение Марса и Земли на момент 2026-08-23.")
plt.axis("equal")
plt.grid()
plt.show()

print(mars["inclination"])