from flask import request, app
import requests
def readdata():
    url = 'http://192.168.1.127:80/sensor_data'
    res = requests.get(url, timeout=0.5)
    print(res.text)

readdata()

if __name__ == 'main':
    app.run()