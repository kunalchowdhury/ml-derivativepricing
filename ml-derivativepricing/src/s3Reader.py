#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:13:00 2023

@author: kunal
"""
import boto3
import csv
import json

def read_file_from_s3():
    s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAYEYVUNNZFHNOVWWN',
    aws_secret_access_key='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',
    region_name='us-east-1'
    ) #1

    obj = s3.get_object(Bucket='marketsworkshop', Key='basket_with_five.csv') #2
    data = obj['Body'].read().decode('utf-8-sig').splitlines() #3
    records = csv.DictReader(data) #4
    headers = next(records) #5
    for eachRecord in records: #6
        print(json.dumps(eachRecord)+'\n')
read_file_from_s3()

#AKIAYEYVUNNZBZM5AP7P
#aNofBoKUkBRVl1NywWftDPCJdAt5KIe0C6E3gJhO