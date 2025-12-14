from skyfield.api import load, EarthSatellite, wgs84
import requests
import geocoder
satname = input("Enter SATELLITE NAME (e.g., ISS (ZARYA), all caps when you spell the man name): ")
ip = geocoder.ip('me')
ts = load.timescale()
t = ts.now()
def get_iss_tle():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url)
    lines = response.text.splitlines()

    for i in range(len(lines)):
        if satname.upper() in lines[i]:
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
    latitude_degrees=ip.lat,
    longitude_degrees=ip.lng,
    elevation_m=30
)
difference = sat - observer
topocentric = difference.at(t)
alt, az, distance = topocentric.altaz()
print("YOUR ESTIMATED LOCATION:", ip.latlng)
if alt.degrees > 0:
    print("SATELLITE IS VISIBLE TO EYE")
else:
    print("SATELLITE IS NOT VISIBLE TO EYE")
print("SATELLITE:", sat)
print("LATITUDE:", subpoint.latitude.degrees)
print("LONGITUDE:", subpoint.longitude.degrees)
print("ELEVATION (km):", subpoint.elevation.km)