#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 09:59:08 2023

@author: kunal
"""
import numpy as np
import pandas as pd

def generate_forward_stock_prices(size):
    return 100 * np.random.lognormal(0.5, 0.25, size)

def generate_stock_vols(size):
    return np.random.uniform(0, 1, size)

def generate_maturity_in_months(size):
    return 0.0328767 * np.random.uniform(0, 43, size)**2

def generate_correlations(size):
    return 2 * (np.random.beta(5, 2, size) -0.5)

def generate_dataset(row, col, inst_id_start):
    d = []
    ids = []
    for i in range(row):
        ids.append(int(inst_id_start + i));
    d.append(ids)    
    for i in range(col):
        forward_prices = generate_forward_stock_prices(row)
        d.append(forward_prices)
    for i in range(col):
        vols = generate_stock_vols(row)
        d.append(vols)
    num_of_corrs = int(col*(col -1)/2)
    for i in range(num_of_corrs):
        corrs = generate_correlations(row)
        d.append(corrs)
    d.append(generate_maturity_in_months(row))    
    return d

d = generate_dataset(1000, 6, 123)
ar = np.array(d).transpose().tolist()
df = pd.DataFrame(ar, columns = ['instrument_id', 
                                 'forward_price_1', 
                                 'forward_price_2',
                                 'forward_price_3',
                                 'forward_price_4', 
                                 'forward_price_5',
                                 'forward_price_6',
                                 'vol_1', 
                                 'vol_2',
                                 'vol_3', 
                                 'vol_4',
                                 'vol_5', 
                                 'vol_6',
                                 'corr_1', 
                                 'corr_2',
                                 'corr_3', 
                                 'corr_4',
                                 'corr_5', 
                                 'corr_6',
                                 'corr_7', 
                                 'corr_8',
                                 'corr_9',
                                 'corr_10', 
                                 'corr_11',
                                 'corr_12', 
                                 'corr_13',
                                 'corr_14', 
                                 'corr_15',
                                 'maturity_in_months'])
print(df)
df.to_csv('test_data_3.csv');

        
    