#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 18:34:31 2023

@author: kunal
"""
import csv

from simple_basket import SimpleBasket

fields = ['instrument_id', 
         'symbol',
         'strike',
         'underlying_symbol_1', 
         'underlying_symbol_2',
         'underlying_symbol_3',
         'underlying_symbol_4',
         'underlying_symbol_5',
         'underlying_symbol_6',
         'expiry', 
         'execution_style', 
         'option_type', 
         'underlying_spot_1', 
         'underlying_spot_2',
         'underlying_spot_3',
         'underlying_spot_4',
         'underlying_spot_5',
         'underlying_spot_6', 
         'underlying_vol_1',
         'underlying_vol_2',
         'underlying_vol_3',
         'underlying_vol_4',
         'underlying_vol_5',
         'underlying_vol_6',
         'corr_11', 
         'corr_12',
         'corr_13',
         'corr_14',
         'corr_15',
         'corr_16', 
         'corr_21', 
         'corr_22',
         'corr_23',
         'corr_24',
         'corr_25',
         'corr_26',
         'corr_31', 
         'corr_32',
         'corr_33',
         'corr_34',
         'corr_35',
         'corr_36',
         'corr_41', 
         'corr_42',
         'corr_43',
         'corr_44',
         'corr_45',
         'corr_46',
         'corr_51', 
         'corr_52',
         'corr_53',
         'corr_54',
         'corr_55',
         'corr_56',
         'corr_61', 
         'corr_62',
         'corr_63',
         'corr_64',
         'corr_65',
         'corr_66',
         'earliest_date', 
         'latest_date', 
         'payoff_at_expiry', 
         'npv' ]    
filename = 'real_basket_options.csv'

def generate_baskets(arr, n, r):
    symbols = []
    data = [0]*r
    generate_baskets_inner(arr, data, 0,n - 1, 0, r, symbols)
basketlist = []
def generate_baskets_inner(arr, data, start,
                    end, index, r, symbols):
                        
    if (index == r):
        sym = []
        for j in range(r):
            sym.append(data[j])
        print(sym)
        basket = SimpleBasket(filename, 'hist_stock_prices.csv','hist_vols.csv', sym)
        basketlist.append( 
                       basket.instrument_id + "," +
                       basket.symbol + "," +
                       str(basket.strike) + "," +
                       ",".join(sym) + "," +
                       str(basket.expiry) + "," + 
                       basket.execution_style + "," + 
                       basket.option_type + "," +
                       ",".join(map(str, basket.underlying_spots))+ "," +
                       ",".join(map(str, basket.underlying_vols))+ "," +
                       ",".join(map(str, basket.underlying_corr_mat))+ "," +
                       str(basket.earliest_date)+ "," +
                       str(basket.latest_date)+ "," +
                       str(basket.payoff_at_expiry) + "," + 
                       str(basket.calculateNPV())
                       
                       )
           # csvfile.close()
        return
    i = start;
    while(i <= end and end - i + 1 >= r - index):
        data[index] = arr[i];
        generate_baskets_inner(arr, data, i + 1,
                        end, index + 1, r, symbols);
        i += 1;


symbols = ['AAPL','ABBV','AXP','BRK','CAT','GS','HON','HD','INTC','JNJ','JPM','KO','MSFT','ORCL','PG']
r = 6;
n = len(symbols);
generate_baskets(symbols, n, r);
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for basket in basketlist:
        csvwriter.writerow(basket.split(","))
    csvfile.close()


# This code is contributed by mits
