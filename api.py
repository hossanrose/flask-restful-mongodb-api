# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "iot_db"
mongo = PyMongo(app, config_prefix='MONGO')

class Devices(Resource):
    def get(self, device_key=None):
        data = []

        if device_key:
            cursor = mongo.db.device.find({"device_key": device_key}, {"_id": 0}).limit(10)
            for device in cursor:
                data.append(device)

            return jsonify({"device": device_key, "response": data})

        else:
            cursor = mongo.db.device.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for device in cursor:
                print device
                data.append(device)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            data['Time'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
            print data
            mongo.db.device.insert(data)

        return redirect(url_for("device"))

class Index(Resource):
    def get(self):
        return redirect(url_for("device"))


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Devices, "/api", endpoint="device")
api.add_resource(Devices, "/api/<string:device_key>", endpoint="device_key")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
