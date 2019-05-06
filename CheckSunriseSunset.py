import time
import requests
from datetime import datetime


def get_current_time():
    r = requests.get(url='http://worldtimeapi.org/api/timezone/Etc/UTC')
    return datetime.strptime(r.json()['datetime'], '%Y-%m-%dT%H:%M:%S.%f%z')


def get_sunrise_sunset(lat, lng):
    r = requests.get(url=f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0")
    json_data = r.json()
    tf = '%Y-%m-%dT%H:%M:%S%z'
    sunrise = datetime.strptime(json_data['results']['sunrise'], tf)
    sunset = datetime.strptime(json_data['results']['sunset'], tf)
    return sunrise, sunset


def is_sun_up():
    sunrise, sunset = get_sunrise_sunset("35.149532", "-90.048981")
    current_time = get_current_time()
    print(f'Current: {current_time} - Sunrise: {sunrise} - Sunset: {sunset}')
    return sunrise < current_time < sunset


def main():
    while True:
        if is_sun_up():
            print(f'The sun is up')
        else:
            print(f'The sun is down')
        time.sleep(600)


main()