#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:41:09 2023

@author: kunal
"""
    s3 = boto3.client('s3',aws_access_key_id='AKIAYEYVUNNZBZM5AP7P',aws_secret_access_key='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',region_name='us-east-1') #1
        obj = s3.get_object(Bucket='marketsworkshop', Key='basket_with_five.csv') #2
        data = obj['Body'].read().decode('utf-8-sig').splitlines() #3
        records = csv.DictReader(data) #4
    #   headers = next(records) #5
        for eachRecord in records: #6
            print(json.dumps(eachRecord)+'\n')
            
 #       obj = s3.get_object(Bucket='marketsworkshop', Key='basket_with_five.csv')["Body"].read()
 #       data = obj['Body'].read().decode('utf-8-sig').splitlines()
 #       spots = [100., 100., 100., 100., 100.]
 #       vols = [0.1, 0.12, 0.13, 0.09, 0.11]
 #       corr_mat = [[1, 0.1, -0.1, 0, 0], [0.1, 1, 0, 0, 0.2], [-0.1, 0, 1, 0, 0], [0, 0, 0, 1, 0.15], [0, 0.2, 0, 0.15, 1]]
 #       b = BasketInstrumentWrapper("123", "Call", 100, "European", 1, 5, spots, vols, corr_mat,0, 0, "False" )
 #       print(b.calculateNPV())

 #       return "SUCCESS "+str(b.calculateNPV())
        return "SUCCESS"
    