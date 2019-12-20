from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer() # more info : https://goo.gl/U2Uwz2
X=cancer['data']
y=cancer['target']
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
print(X_train.shape)
print(X_test)

#from sklearn.neural_network import MLPClassifier
#mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
#import tensorflow as tf
import tensorflow.keras as keras
import tensorflow as tf

model = keras.Sequential([
    keras.layers.Dense(30, activation=tf.nn.relu,
                       input_shape=(X_train.shape[1],)),
    keras.layers.Dense(30, activation=tf.nn.relu),
    keras.layers.Dense(30, activation=tf.nn.relu),
    keras.layers.Dense(30, activation=tf.nn.relu),
    keras.layers.Dense(1)
  ])

import os
path = "modelcp/cp-cancer-{epoch:04d}-{loss:.6f}.ckpt"
mcpcb = tf.keras.callbacks.ModelCheckpoint(filepath=path,
                                         save_weights_only=True,
                                         save_best_only=True,
                                         monitor='loss',
                                         verbose=1)

#model.compile(loss="mse", optimizer="sgd")
#sgd = keras.optimizers.SGD(nesterov=True, lr=1e-5)
model.compile(loss="mse", optimizer="adam",metrics = ['mean_squared_error'])
model.summary()

history = model.fit(X_train, y_train, epochs=2000, callbacks=[mcpcb])
eval = model.evaluate(X_test, y_test)
print(eval)
model.save("cancer.h5")
