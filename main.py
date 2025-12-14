from skyfield.api import load, EarthSatellite, wgs84
import requests
import geocoder
ts = load.timescale()
t = ts.now()
def get_iss_tle():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url)
    lines = response.text.splitlines()

    for i in range(len(lines)):
        if "ISS (ZARYA)" in lines[i]:
            name = lines[i]
            line1 = lines[i + 1]
            line2 = lines[i + 2]
            return name, line1, line2

    raise Exception("ISS TLE bulunamadı")
name, line1, line2 = get_iss_tle()
sat = EarthSatellite(line1, line2, name, ts)
pos = sat.at(t)
subpoint = wgs84.subpoint(pos)
observer = wgs84.latlon(
    latitude_degrees=41.0082,
    longitude_degrees=28.9784,
    elevation_m=30
)

print("SATELLITE:", sat)
print("LATITUDE:", subpoint.latitude.degrees)
print("LONGITUDE:", subpoint.longitude.degrees)
print("ELEVATION (km):", subpoint.elevation.km)