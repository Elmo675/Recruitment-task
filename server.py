#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)


class Order(Resource):
    def post(self):
        print(request.json)
        Type = request.json['type']
        Url  = request.json['url']
        return {'status':'success', 'type' : Type, 'url' : Url }

    
class Order_Result(Resource):
    def get(self, order_id):
        return None

    
class Order_Status(Resource):
    def get(self, order_id):
        return None


api.add_resource(Order, '/order') # Route_1
api.add_resource(Order_Status, '/order-status/<order_id>') # Route_2
api.add_resource(Order_Result, '/order-result/<order_id>') # Route_3



if __name__ == '__main__':
     app.run()

