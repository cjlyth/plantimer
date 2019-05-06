# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, jsonify
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

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def check_is_sun_up():
    """Return a friendly HTTP greeting."""
    return jsonify(sun_is_up=is_sun_up())


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
