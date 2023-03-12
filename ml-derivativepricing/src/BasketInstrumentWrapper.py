#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 06:39:02 2023

@author: kunal
"""
import QuantLib as ql 
ql.__version__

    
class BasketInstrumentWrapper:
    strike_price =""
    option_type = ""
    execution_style = ""
    expiration = 0
    number_of_instruments = 0
    instrument_id = ""
    underlying_spots = []
    underlying_vols = []
    underlying_corr_mat = []
    earliest_date = 0
    latest_date = 0
    payoff_at_expiry = False
    
    def __init__(self, instrument_id, option_type, strike_price, execution, 
                 expiration_in_yrs , number_of_instruments,underlying_spots,
                 underlying_vols, underlying_corr_mat,
                 earliest_date,latest_date,payoff_at_expiry):
        self.strike_price = strike_price
        self.option_type = option_type
        self.execution_style = execution
        self.expiration = expiration_in_yrs
        self.number_of_instruments = number_of_instruments
        self.instrument_id = instrument_id
        self.underlying_spots = underlying_spots
        self.underlying_vols = underlying_vols
        self.underlying_corr_mat = underlying_corr_mat
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.payoff_at_expiry = payoff_at_expiry
        
    def display(self):
        print("instrument_id = "+ str(self.instrument_id))
        print("number of instrument = "+ str(self.number_of_instruments))
        print("expiration = "+ str(self.expiration))
        print("execution = "+str(self.execution_style))
        print("option type = "+ str(self.option_type))
        print("strike price = "+ str(self.strike_price))
    
    def calculateNPV(self):
        underlying_spots = self.underlying_spots
        underlying_vols = self.underlying_vols
        underlying_corr_mat = self.underlying_corr_mat
        expiration = self.expiration
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
        engine = ql.MCEuropeanBasketEngine(multiProcess, rng, timeStepsPerYear=stepsPerYear, requiredSamples=numSteps, seed=seed)
        
        today = ql.Date().todaysDate()
        exp_date = today + ql.Period(expiration, ql.Months)
        strike = self.strike_price
        number_of_underlyings = self.number_of_instruments
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

#spots = [100., 100., 100., 100., 100.]
#vols = [0.1, 0.12, 0.13, 0.09, 0.11]
#corr_mat = [[1, 0.1, -0.1, 0, 0], [0.1, 1, 0, 0, 0.2], [-0.1, 0, 1, 0, 0], [0, 0, 0, 1, 0.15], [0, 0.2, 0, 0.15, 1]]
#b = BasketInstrumentWrapper("123", "Call", 100, "European", 1, 5, spots, vols, corr_mat, )
#print(b.calculateNPV())


        
        
        
        
        