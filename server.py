#!/usr/bin/python3
from flask import Flask, request
from flask_restful import Resource, Api
from logic import Task
app = Flask(__name__)
api = Api(app)

#Global variable
task = None

class Order(Resource):
    def post(self):
        global task
        try:
            Type = request.json['type']
            Url  = request.json['url']
        except:
            return {'status':'fail'}
        if Type not in ["text","image"]:
            return {'status':'bad option: text or image needed'}
        task = Task(Type,Url)
        return {'status':'success'}

    
class Order_Result(Resource):
    def get(self):
        global task
        if task is None:
            return {'status':'no tasks to proceed'}
        if task.get_status()!=3:
            return {'status':'not ready'}
        return {'status':'success', 'data':[el for el in task.get_result()]}

    
class Order_Status(Resource):
    def get(self):
        if task is None:
            return {'status':'no tasks to proceed'}
        return {'status':'success','order_status':str(task.INFO[task.get_status()+2])}


api.add_resource(Order, '/order') # Route_1
api.add_resource(Order_Status, '/order-status') # Route_2
api.add_resource(Order_Result, '/order-result') # Route_2



if __name__ == '__main__':
     app.run()
