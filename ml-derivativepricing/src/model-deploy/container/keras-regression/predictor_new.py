# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import io
import json
import os
import pickle
import signal
import sys
import traceback
import boto3
import flask
import pandas as pd
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from matplotlib.pylab import plt
from flask_cors import CORS, cross_origin
from flask import Flask

app = Flask(__name__)
CORS(app)

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


class PricingService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            with open(os.path.join(model_path, "decision-tree-model.pkl"), "rb") as inp:
                cls.model = pickle.load(inp)
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model()
        return clf.predict(input)


# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to ML-Workshop. This is Team1 calling</p>"


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = PricingService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/evaluate", methods=["POST"])
@cross_origin()
def evaluate():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    valuation_results = {}
    # Convert from CSV to pandas
    
    if flask.request.content_type == "application/json":
        print('Got JSON request')
        #data = flask.request.data.decode("utf-8")
        #s = io.StringIO(data)
        #df = pd.read_csv(s)
        #res = df.to_json(orient="records")
        #parsed = json.loads(res)
        parsed = flask.request.get_json()
        lambda_client = boto3.client('lambda', aws_access_key_id='AKIAYEYVUNNZCNEXLGU5' ,aws_secret_access_key='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')
        print('Lambda client initialized') 
        valuation_results['from_quantlib'] = {}
        instruments = []
        for dict in parsed:
            try:
                #print(dict)
                invoke_response = lambda_client.invoke(FunctionName='execValuation',
                                  InvocationType='RequestResponse',
                                  Payload=json.dumps(dict))
                npv = invoke_response['Payload'].read().decode()
                print('npv = ' + npv)
                instruments.append(dict["instrument_id"])
                valuation_results['from_quantlib'][dict["instrument_id"]] = npv 
            except Exception as e:
                  print(e)  
        valuation_results['from_keras'] = {}
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        cols_to_keep =['und_spot_1',
                       'und_spot_2',
                       'und_spot_3',
                       'und_spot_4',
                       'und_spot_5',
                       'und_spot_6',
                       'und_vol_1',
                       'und_vol_2',
                       'und_vol_3',
                       'und_vol_4',
                       'und_vol_5',
                       'und_vol_6',
                       'corr_12',
                       'corr_13',
                       'corr_14',
                       'corr_15',
                       'corr_16',
                       'corr_23',
                       'corr_24',
                       'corr_25',
                       'corr_26',
                       'corr_34',
                       'corr_35',
                       'corr_36',
                       'corr_45',
                       'corr_46',
                       'corr_56',
                       'expiration_in_mnths']
        valuation_results['diff_pc'] = {}
        for dict in parsed:
            try:
                ins_id = dict['instrument_id']
                res = [val for key, val in dict.items() if key in cols_to_keep]
                #print(type(res))
                #input_list = list(res.values())
                X_val = []
                for v in res:
                    i_l = [v]
                    X_val.append(i_l)
                #scaler = MinMaxScaler()
                #print(X_val)    
                #X_scaled2 = scaler.fit_transform(X_val)
                #predicted_npv = loaded_model.predict(np.array([X_scaled2]))
                predicted_npv = loaded_model.predict(np.array([X_val]))
                #print(predicted_npv)
                valuation_results['from_keras'][ins_id] = str(predicted_npv[0][0]) 
                diff = 0;
                if predicted_npv > float(valuation_results['from_quantlib'][ins_id]):
                    diff = (predicted_npv[0][0] - float(valuation_results['from_quantlib'][ins_id]))/predicted_npv[0][0]
                else:
                    diff = (float(valuation_results['from_quantlib'][ins_id]) - predicted_npv[0][0])/float(valuation_results['from_quantlib'][ins_id])
                valuation_results['diff_pc'][ins_id] = str(diff * 100)
                
            except Exception as e:
                  print(e)
      
        # Response data           
        final_data = {}
        final_data['data']=[]
        actual_dict ={}
        pred_dict={}
        i = 0
        for r in valuation_results['from_quantlib']:
            ins_data ={}
            ins_data['instrumentId'] = r
            ins_data['actual']= valuation_results['from_quantlib'][r]
            ins_data['predicted']= valuation_results['from_keras'][r]
            ins_data['diff']= valuation_results['diff_pc'][r]
    
            actual_dict[i] =  round(ins_data['actual'], 2)
            pred_dict[i] = round(ins_data['predicted'],2)
            i = i + 1
            final_data['data'].append(ins_data) 
        
        # Plot and label the actual and validation loss values
        actual_values = actual_dict.values()
        pred_values = pred_dict.values()
        plt.figure(figsize=(8,8))
        plt.scatter(actual_values, pred_values, c='crimson')
        plt.yscale('log')
        plt.xscale('log')

        p1 = max(max(pred_values), max(actual_values))
        p2 = min(min(pred_values), min(actual_values))
        #plt.plot([p1, p2], [p1, p2], 'b-')
        plt.xlabel('Actual Values', fontsize=15)
        plt.ylabel('Predictions', fontsize=15)
        plt.axis('equal')
        
        dataplot = io.BytesIO()
        plt.savefig(dataplot,format='png')
        dataplot.seek(0)
       
        s3 = boto3.resource('s3', aws_access_key_id='AKIAYEYVUNNZCNEXLGU5' ,aws_secret_access_key='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',region_name='us-east-1')
        bucket = s3.Bucket("marketsworkshop")
        bucket.put_object(Body=dataplot, ContentType='image/png',Key="mldata/dataplot.png",ACL='public-read')
        
        final_data['pltImg'] = 'https://marketsworkshop.s3.amazonaws.com/mldata/dataplot.png'

    else:
        return flask.Response(
            response="This predictor only supports CSV data", status=415, mimetype="text/plain"
        )

    #print("Invoked with {} records".format(data.shape[0]))

    # Do the prediction
    #predictions = PricingService.predict(data)

    # Convert from numpy back to CSV
    #out = io.StringIO()
    #pd.DataFrame({"quantlib-npv": npv}).to_csv(out, header=False, index=False)
    
    #result = out.getvalue()

    return flask.Response(response=json.dumps(final_data), status=200, mimetype="json")
