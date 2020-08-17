from flask import Flask, request, Response, render_template
from wsgiref import simple_server
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from TrainingValidationInsertion import TrainValidation
from TrainingModel import TrainModel
from PredictionValidationInsertion import PredictionValidation
from PredictionFromModel import Prediction
#from datetime import datetime

os.putenv('LANG','en_US.UTF-8')
os.putenv('LC_ALL','en_US.UTF-8')


app=Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/",methods=['GET'])
@cross_origin()
def home():
    return render_template('page.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    print('Hello Predict')
    try:
        # This request is for "Postman" which is used for testing purpose
        if request.json is not None:
            path = request.json['filepath']

            pred_val = PredictionValidation(path) #object initialization

            pred_val.PredictionValidation() #calling the prediction_validation function

            pred = Prediction(path) #object initialization

            #predicting for dataset present in database
            #path,json_predictions = pred.PredictionFromModel()
            path = pred.PredictionFromModel()
            # return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
            return Response("Prediction File created at !!!" + str(path))
        #This is for Web
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = PredictionValidation(path) #object initialization

            pred_val.PredictionValidation() #calling the prediction_validation function

            pred = Prediction(path) #object initialization

            # predicting for dataset present in database
            #path,json_predictions = pred.PredictionFromModel()
            path = pred.PredictionFromModel()
            #return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
            return Response("Prediction File created at !!!" + str(path))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    print('Hello Train')

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            train_valObj = TrainValidation(path) #object initialization

            train_valObj.TrainValidation()#calling the training_validation function


            trainModelObj = TrainModel() #object initialization
            trainModelObj.TrainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")



port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    host='0.0.0.0'
    #port = 7500
    server_ = simple_server.make_server(host,port,app)
    server_.serve_forever()
    #app.run()

