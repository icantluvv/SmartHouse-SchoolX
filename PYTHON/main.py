from flask import render_template, request, jsonify, app
from model import *
from model import app, db

esp_url = "http://172.20.10.10:80"

data = Data()


def read_data_from_esp():
    try:
        url = f'{esp_url}/sensor_data'
        res = request.get(url, timeout=0.05)
        content = res.text.split("/")
        data = Data(air_temp_c=float(content[0]),
                    humidity=float(content[1]))
        # datetime = datetime.datetime.now()
        db.session.add(data)
        db.session.commit()
        

    except:
        print("Error esp")
        return False


# @app.route('/api/data', methods=['GET'])
# def api_data():
#     data = get_last_data()
#     dict_json = {'datetime': data.datetime}
#     sensors = [{'id': "tempWaterC", 'name': "Температура воды", 'value': data.water_temp_c, 'measure': '°'},
#                {'id': "tempAirC", 'name': "Температура воздуха", 'value': data.air_temp_c, 'measure': '°'},
#                {'id': "humidity", 'name': "Влажность", 'value': data.humidity, 'measure': '%'}]
#     control = [{'id': "pumpState", 'name': "Полив", 'toggleRoute': "/pump/config", 'state': data.pump_state},
#                {'id': "ledState", 'name': "Свет", 'toggleRoute': "/led/config", 'state': data.led_state}]
#     dict_json.update({'sensors': sensors})
#     dict_json.update({'control': control})
#     response = jsonify(dict_json)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

#
# def get_last_data(attempt=0):
#     if attempt > 2:
#         return db.session.query(Data).all()[0]
#     data = db.session.query(Data).all()
#     if data is not None and len(data) > 0:
#         data = data[len(data) - 1]
#         if abs((data.datetime - datetime.datetime.now()).total_seconds()) > 30:
#             read_data_from_esp()
#             return get_last_data(attempt=attempt + 1)
#         else:Ы
#             return data
#     else:
#         read_data_from_esp()
#         return get_last_data(attempt=attempt + 1)


@app.route('/')
def show_main():
    return render_template("main.html", data=data)



if __name__ == '__main__':


    app.app_context().push()

    app.run()
