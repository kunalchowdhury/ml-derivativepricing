#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:39:38 2023

@author: kunal
"""
import json
import urllib.parse
import boto3
import sys
from ctypes import cdll
import csv
import json

#sys.path.append('/opt/python/lib/python3.7/site-packages/QuantLib')

cdll.LoadLibrary('/opt/python/lib/python3.7/site-packages/QuantLib/libQuantLib-f287b9e2.so.0.0.0')
from BasketInstrumentWrapper import BasketInstrumentWrapper
import QuantLib  as ql 
import decimal
ql.__version__


print('Loading function')

#s3 = boto3.client('s3')

#S3_BUCKET = 'marketsworkshop'
def lambda_handler(event, context):
    try:
        b = BasketInstrumentWrapper(event.get('instrument_id'),event.get('option_type'),float(event.get('strike_price')),event.get('execution'),int(event.get('expiration_in_mnths')),int(event.get('number_of_instruments')),[float(event.get('und_spot_1')), float(event.get('und_spot_2')), float(event.get('und_spot_3')), float(event.get('und_spot_4')), float(event.get('und_spot_5'))],[float(event.get('und_vol_1')), float(event.get('und_vol_2')), float(event.get('und_vol_3')), float(event.get('und_vol_4')), float(event.get('und_vol_5'))],[[float(event.get('und_corr_mat_00')), float(event.get('und_corr_mat_01')),float(event.get('und_corr_mat_02')),float(event.get('und_corr_mat_03')),float(event.get('und_corr_mat_04'))],[float(event.get('und_corr_mat_10')), float(event.get('und_corr_mat_11')), float(event.get('und_corr_mat_12')),float(event.get('und_corr_mat_13')),float(event.get('und_corr_mat_14'))],[float(event.get('und_corr_mat_20')), float(event.get('und_corr_mat_21')), float(event.get('und_corr_mat_22')),float(event.get('und_corr_mat_23')),float(event.get('und_corr_mat_24'))],[float(event.get('und_corr_mat_30')),float(event.get('und_corr_mat_31')), float(event.get('und_corr_mat_32')),float(event.get('und_corr_mat_33')),float(event.get('und_corr_mat_34'))],[float(event.get('und_corr_mat_40')),float(event.get('und_corr_mat_41')),float(event.get('und_corr_mat_42')),float(event.get('und_corr_mat_43')),float(event.get('und_corr_mat_44'))]],int(event.get('earliest_date')),int(event.get('latest_date')),bool(event.get('payoff_at_expiry')))
        npv = b.calculateNPV()
        event["price"] = npv
        response = "Instrument Id = " + event.get('instrument_id') + " , Price = "+str(npv)
        print(response) 
        j = json.loads(json.dumps(event), parse_float=decimal.Decimal)
        j = {k: v for k, v in j.items() if v}
        print(j)
        #dynamodb_client = boto3.client("dynamodb")
        #dynamo_resp = dynamodb_client.put_item(TableName="valuation_results",Item = j)
        #print(dynamo_resp)
        database = boto3.resource('dynamodb')
        table = database.Table("valuation_results")
        table.put_item(Item = j)
        #rec = table.get_item(Key={'instrument_id': '124'})
        print(rec['Item']['instrument_id'] + " -> " + str(rec['Item']['price']))
        return npv
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
