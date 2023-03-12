#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:23:41 2023

@author: kunal
"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
import tensorflow as tf
import numpy as np
import time
import sys
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
    model.add(tf.keras.Input(shape=(28, )))
    model.add(BatchNormalization(momentum=0.3))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    return model

def generate_network_old():
    model = Sequential()
    model.add(tf.keras.Input(shape=(28, )))
   # model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(Dense(128))
    model.add(Dense(256, kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    #model.add(Dense(512, activation='relu'))
    model.add(Dense(512,kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    #model.add(Dense(1, activation='relu'))
    model.add(Dense(256,kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4),bias_regularizer=regularizers.l2(1e-4),activity_regularizer=regularizers.l2(1e-5)))
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    return model
EPOCHS = 10000
BS = 100
INIT_LR = 1e-4
model = generate_network()
opt = tf.keras.optimizers.Adam(learning_rate=INIT_LR, weight_decay=INIT_LR / EPOCHS)
#model.compile(optimizer='sgd',loss='cosine_similarity')
#model.compile(optimizer='rmsprop',loss='cosine_similarity')
#model.compile(optimizer='rmsprop',loss='mean_squared_error')
model.compile(optimizer='sgd', loss=tf.keras.losses.LogCosh() )

def step(X, y):
	# keep track of our gradients
	with tf.GradientTape() as tape:
		# make a prediction using the model and then calculate the
		# loss
		pred = model(X)
		loss = mean_squared_error(np.reshape(y, (100, 1)), pred)
	# calculate the gradients using our tape and then update the
	# model weights
	grads = tape.gradient(loss, model.trainable_variables)
	opt.apply_gradients(zip(grads, model.trainable_variables))

dataset = loadtxt('markets_workshop_training_data.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:28]
y = dataset[:,28]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#X_train = np.expand_dims(X_train, axis=-1)
#X_test = np.expand_dims(X_test, axis=-1)

# compute the number of batch updates per epoch
numUpdates = int(X_train.shape[0] / BS)
# loop over the number of epochs
for epoch in range(0, EPOCHS):
	# show the current epoch number
	print("[INFO] starting epoch {}/{}...".format(
		epoch + 1, EPOCHS), end="")
	sys.stdout.flush()
	epochStart = time.time()
	# loop over the data in batch size increments
	for i in range(0, numUpdates):
		# determine starting and ending slice indexes for the current
		# batch
		start = i * BS
		end = start + BS
		# take a step
		step(X_train[start:end], y_train[start:end])
	# show timing information for the epoch
	epochEnd = time.time()
	elapsed = (epochEnd - epochStart) / 60.0
	print("took {:.4} minutes".format(elapsed))

# in order to calculate accuracy using Keras' functions we first need
# to compile the model
# now that the model is compiled we can compute the accuracy
v = model.evaluate(X_test, y_test)
print(v);
print("[INFO] test loss: {:.4f}".format(v))

