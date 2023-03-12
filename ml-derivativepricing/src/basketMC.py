#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:12:13 2023

@author: kunal
"""
import QuantLib as ql 
import matplotlib.pyplot as plt
ql.__version__

# Create a StochasticProcessArray for the various underlyings
underlying_spots = [100., 100., 100., 100., 100.]
underlying_vols = [0.1, 0.12, 0.13, 0.09, 0.11]
underlying_corr_mat = [[1, 0.1, -0.1, 0, 0], [0.1, 1, 0, 0, 0.2], [-0.1, 0, 1, 0, 0], [0, 0, 0, 1, 0.15], [0, 0.2, 0, 0.15, 1]]

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
exp_date = today + ql.Period(1, ql.Years)
strike = 100
number_of_underlyings = 5

exercise = ql.EuropeanExercise(exp_date)
vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)

payoffMin = ql.MinBasketPayoff(vanillaPayoff)
basketOptionMin = ql.BasketOption(payoffMin, exercise)

payoffAverage = ql.AverageBasketPayoff(vanillaPayoff, number_of_underlyings)
basketOptionAverage = ql.BasketOption(payoffAverage, exercise)

payoffMax = ql.MaxBasketPayoff(vanillaPayoff)
basketOptionMax = ql.BasketOption(payoffMax, exercise)


basketOptionMin.setPricingEngine(engine);
print(basketOptionMin.NPV())
