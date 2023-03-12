#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:37:01 2023

@author: kunal
"""
from BasketInstrumentWrapper import BasketInstrumentWrapper
import csv
import pandas as pd
class InstrumentReader:
    file = ""
    list_of_instrument_wrapper = []
    def __init__(self, file):
        self.file = file
    def parse_instruments(self):
        with open(self.file, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                b = BasketInstrumentWrapper(row['instrument_id'], 
                                        row['option_type'],
                                        float(row['strike_price']),
                                        row['execution'],
                                        int(row['expiration_in_mnths']), 
                                        int(row['number_of_instruments']), 
                                        [float(row['und_spot_1']), float(row['und_spot_2']), float(row['und_spot_3']), float(row['und_spot_4']), float(row['und_spot_5'])], 
                                        [float(row['und_vol_1']), float(row['und_vol_2']), float(row['und_vol_3']), float(row['und_vol_4']), float(row['und_vol_5'])],
                                        [[float(row['und_corr_mat_00']), 
                                          float(row['und_corr_mat_01']), 
                                          float(row['und_corr_mat_02']), 
                                          float(row['und_corr_mat_03']), 
                                          float(row['und_corr_mat_04'])],
                                         [float(row['und_corr_mat_10']), 
                                           float(row['und_corr_mat_11']), 
                                           float(row['und_corr_mat_12']), 
                                           float(row['und_corr_mat_13']), 
                                           float(row['und_corr_mat_14'])],
                                         [float(row['und_corr_mat_20']), 
                                          float(row['und_corr_mat_21']), 
                                          float(row['und_corr_mat_22']), 
                                          float(row['und_corr_mat_23']), 
                                          float(row['und_corr_mat_24'])],
                                         [float(row['und_corr_mat_30']), 
                                          float(row['und_corr_mat_31']), 
                                          float(row['und_corr_mat_32']), 
                                          float(row['und_corr_mat_33']), 
                                          float(row['und_corr_mat_34'])],
                                         [float(row['und_corr_mat_40']), 
                                          float(row['und_corr_mat_41']), 
                                          float(row['und_corr_mat_42']), 
                                          float(row['und_corr_mat_43']), 
                                          float(row['und_corr_mat_44'])]],
                                         int(row['earliest_date']),
                                         int(row['latest_date']),
                                         bool(row['payoff_at_expiry'])
                                
                                        ) 
                self.list_of_instrument_wrapper.append(b)
        
    def invoke_valuation(self):
        d = []
        for instrument in self.list_of_instrument_wrapper:
            print("Instrument Id = "+ instrument.instrument_id+", Price = "+str(instrument.calculateNPV()))
            d.append((instrument.instrument_id, instrument.calculateNPV()))
        df = pd.DataFrame(d, columns=['instrument_id', 'calculated_price'])
        df.to_csv("calculated_prices.csv")


reader = InstrumentReader("/Users/kunal/pricing_data/instrument_nos_5/basket_with_five_all_temp.csv")
reader.parse_instruments()
reader.invoke_valuation()

                                                                                                                                                                                                                                                                                                                     

    