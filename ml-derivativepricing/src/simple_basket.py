#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:33:47 2023

@author: kunal
"""
import QuantLib as ql 
ql.__version__
import uuid 
import random
import pandas as pd
import numpy as np

class SimpleBasket:
    instrument_id = ''
    symbol = ''
    underlying_symbols = []
    expiry = 0
    execution_style = ''
    option_type = ''
    underlying_spots = []
    underlying_vols = []
    underlying_corr_mat = []
    earliest_date = 0
    latest_date = 0
    payoff_at_expiry = False
    file = ''
    expiries = [3, 6, 9, 12]
    exec_types = ['American', 'European']
    option_types = ['Call', 'Put']
    payoff_at_expiries = [False]
    corr_mat = []
    strike = 0
    
    def __init__(self, filePath, stock_prices, stock_vols, symbols):
        self.file = filePath
        df_prices = pd.read_csv(stock_prices)
        df_vols = pd.read_csv(stock_vols)
        self.instrument_id = uuid.uuid4().hex[:24]
        self.symbol = 'BSK-' + '-'.join(symbols)
        self.underlying_symbols = symbols
        self.expiry = random.choice(self.expiries)
        self.execution_style = random.choice(self.exec_types)
        self.option_type = random.choice(self.option_types)
        i = 0;
        self.corr_mat = [[0]*len(symbols) for i in range(len(symbols))]
        self.underlying_spots.clear()
        self.underlying_vols.clear()
        self.underlying_corr_mat.clear()
        for symbol in symbols:
            self.underlying_spots.append(df_prices[symbol][0])
            self.underlying_vols.append(df_vols[symbol][0])
            j = 0;
            for inner_symbol in symbols:
                if(symbol == inner_symbol):
                    self.corr_mat[i][j] = 0
                    self.underlying_corr_mat.append(0)
                else:
                    s1 = pd.Series(df_prices[symbol])
                    s2 = pd.Series(df_prices[inner_symbol])
                    self.underlying_corr_mat.append(s1.corr(s2))
                    self.corr_mat[i][j] = s1.corr(s2);
                j = j+1;
            i = i+1;
        if self.option_type == 'Call':
            self.strike = np.min(self.underlying_spots) - +0.5
        else:
            self.strike = np.max(self.underlying_spots) - 0.5
        
        e_l_expiries = random.sample(self.expiries, 2)
        e_l_expiries.sort()
        self.earliest_date = e_l_expiries[0]
        self.latest_date = e_l_expiries[1]
        self.payoff_at_expiry = random.choice(self.payoff_at_expiries)
        
    
    def calculateNPV(self):
        try:
            underlying_spots = self.underlying_spots
            underlying_vols = self.underlying_vols
            underlying_corr_mat = self.corr_mat
            expiration = self.expiry
            today = ql.Date().todaysDate()
            day_count = ql.Actual365Fixed()
            calendar = ql.NullCalendar()
            riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count))
            dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count))
            processes = [ql.BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(x)),
                                                      dividendTS,
                                                      riskFreeTS,
                                                      ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, y, day_count)))
                         for x, y in zip(underlying_spots, underlying_vols)]
    
            multiProcess = ql.StochasticProcessArray(processes, underlying_corr_mat)
    
            # Create the pricing engine
            rng = "pseudorandom"
            numSteps = 500000
            stepsPerYear = 1
            seed = 43
            if self.execution_style == 'American':
                engine = ql.MCAmericanBasketEngine(multiProcess, rng, timeStepsPerYear=stepsPerYear, requiredSamples=numSteps, seed=seed)
            else:
                engine = ql.MCEuropeanBasketEngine(multiProcess, rng, timeStepsPerYear=stepsPerYear, requiredSamples=numSteps, seed=seed)
            
            today = ql.Date().todaysDate()
            exp_date = today + ql.Period(expiration, ql.Months)
            strike = self.strike
            number_of_underlyings = len(self.underlying_symbols)
            exercise = ql.EuropeanExercise(exp_date)
            
            if self.execution_style == 'American':
                earliest_dt = today + ql.Period(self.earliest_date, ql.Months)
                latest_dt = today + ql.Period(self.latest_date, ql.Months)
                exercise = ql.AmericanExercise(earliest_dt, latest_dt , self.payoff_at_expiry)
          
            vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
            if self.option_type == 'Put':
                vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Put, strike)
                
            payoffAverage = ql.AverageBasketPayoff(vanillaPayoff, number_of_underlyings)
            basketOptionAverage = ql.BasketOption(payoffAverage, exercise)
            basketOptionAverage.setPricingEngine(engine)
            return basketOptionAverage.NPV();
        except Exception as e:
            print(e)
            print(self.instrument_id + " , "+self.option_type)
            #print(self.corr_mat)
            #print(processes)
            #print(underlying_vols)
            #print(underlying_spots)
            raise e


        




