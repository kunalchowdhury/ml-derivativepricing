#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 14:29:54 2023

@author: kunal
"""
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Flatten
from tensorflow.keras import regularizers
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import BatchNormalization
import numpy as np
import tensorflow as tf

def generate_network():
    model = Sequential()
    model.add(Flatten(input_shape=(28,)))
    model.add(Dense(256,kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(LeakyReLU(alpha=0.4))
    model.add(BatchNormalization(momentum=0.4))
    model.add(Dense(512,kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(LeakyReLU(alpha=0.4))
    model.add(BatchNormalization(momentum=0.4))
    model.add(Dense(1,kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(LeakyReLU(alpha=0.4))
    model.add(BatchNormalization(momentum=0.4))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=[tf.keras.metrics.MeanSquaredError(),
                       tf.keras.metrics.FalseNegatives()])
    model.summary()
    return model


# load the dataset
dataset = loadtxt('markets_workshop_training_data.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:28]
y = dataset[:,28]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

# define the keras model
model = generate_network()
#model.add(Dense(12, input_shape=(28,), activation='relu'))
#model.add(Dense(8, activation='relu'))
#model.add(Dense(1, activation='sigmoid'))
# compile the keras model
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X_train, y_train, epochs=1000, batch_size=100)
# evaluate the keras model
accuracy = model.evaluate(X_test, y_test)
print(accuracy*100)