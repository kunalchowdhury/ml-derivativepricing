#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:51:19 2023

@author: kunal
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import beta

def generate_forward_stock_prices(mu, std, size):
    return mu * np.random.lognormal(0, 1, size)

def generate_stock_vols(lo, hi, size):
    return np.random.uniform(lo, hi, size)

def generate_maturity_in_months(mu, std, size):
    return np.random.uniform(mu, std, size)**2

def generate_correlations(alpha, beta, size):
    return 2 * (np.random.beta(alpha, beta, size) -0.5)

stocks_fields = ['underlying_spot_1', 
                 'underlying_spot_2',	
                 'underlying_spot_3', 
                 'underlying_spot_4',	
                 'underlying_spot_5',	
                 'underlying_spot_6']
vol_fields = ['underlying_vol_1',	
              'underlying_vol_2',	
              'underlying_vol_3',	
              'underlying_vol_4',	
              'underlying_vol_5',	
              'underlying_vol_6']
corr_fields = ['corr_12','corr_13','corr_14','corr_15','corr_16',	
               'corr_23','corr_24','corr_25','corr_26',	
               'corr_34','corr_35','corr_36',	
               'corr_45','corr_46',	
               'corr_56'	
               ]
outfilename = 'hist_data_for_network_training.csv'

def generate_dataset(valuation_file_name, row, col):
    try:
        d = []
        ids = []
        df = pd.read_csv(valuation_file_name)
        for i in range(col):
            fld = stocks_fields[i]
            mu, std = norm.fit(df[fld])
            #print(str(mu) +" ,  "+ str(std))
            forward_prices = generate_forward_stock_prices(mu, std, row)
            d.append(forward_prices)
        for j in range(col):
            fld = vol_fields[j]
            lo = np.min(df[fld])
            hi = np.max(df[fld])
            vols = generate_stock_vols(lo, hi, row)
            d.append(vols)
        num_of_corrs = int(col*(col -1)/2)
        for k in range(num_of_corrs):
            #print(k)
            fld = corr_fields[k]
            alpha, bet, loc, scale = beta.fit(df[fld])
            #print(str(alpha) + " , "+str(bet))
            corrs = generate_correlations(alpha, bet, row)
            d.append(corrs)
        dts = [3, 6, 9, 12]
        mu, std = norm.fit(dts)
        d.append(generate_maturity_in_months(mu, std, row))   
        d.append(df['npv'].to_numpy())
        return d
    except Exception as e:
        print(e)

d = generate_dataset('real_basket_options.csv', 5005, 6)
ar = np.array(d).transpose().tolist()
df = pd.DataFrame(ar, columns = ['forward_price_1', 
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
                                 'maturity_in_months', 
                                 'price'])
#print(df)
df.to_csv('historical_test_data_with_header.csv',header=True, index=False);
print('Data generation complete !')

    
    
    