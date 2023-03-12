#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:50:55 2023

@author: kunal
"""
# first neural network with keras tutorial
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
# load the dataset
dataset = loadtxt('markets_workshop_training_data.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:28]
y = dataset[:,28]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

# define the keras model
model = Sequential()
model.add(Dense(12, input_shape=(28,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X_train, y_train, epochs=1000, batch_size=10)
# evaluate the keras model
_, accuracy = model.evaluate(X_test, y_train)
print('Accuracy: %.2f' % (accuracy*100))