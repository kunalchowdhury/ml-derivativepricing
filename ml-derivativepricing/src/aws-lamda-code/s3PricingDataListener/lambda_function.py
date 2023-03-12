#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:42:55 2023

@author: kunal
"""
import json
import urllib.parse
import boto3
import csv
print('Loading function')


def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3',aws_access_key_id='AKIAYEYVUNNZBZM5AP7P',aws_secret_access_key='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',region_name='us-east-1') #1
        obj = s3.get_object(Bucket='marketsworkshop', Key='basket_with_five.csv') #2
        data = obj['Body'].read().decode('utf-8-sig').splitlines() #3
        records = csv.DictReader(data) #4
        lambda_client = boto3.client('lambda')
        for eachRecord in records: #6
            print(json.dumps(eachRecord)+'\n')
            lambda_client.invoke(FunctionName='execValuation', 
                     InvocationType='RequestResponse',
                     Payload=json.dumps(eachRecord))
        return 'SUCCESS'
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
