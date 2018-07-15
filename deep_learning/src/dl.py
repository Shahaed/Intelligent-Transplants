from numpy import loadtxt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import time
import datetime
from sklearn.svm import SVC
# from xgboost import XGBClassifier
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import TensorBoard
from keras.utils import plot_model
from keras.optimizers import adam

from keras.layers.core import Activation, Flatten
from keras.layers.convolutional import Conv2D
import h5py
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from keras import backend as K
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
import pandas as pd
import tensorflow as tf
from keras.models import load_model
import matplotlib.pyplot as plt
import pydot


# age_don,hgt_cm_don_calc,wgt_kg_don_calc,ethcat_don,hist_hypertens_don,hist_diabetes_don,cod_cad_don,creat_don,hep_c_anti_don,non_hrt_don,bmis,drmis,txkid,tx_procedur_ty_ki,cold_isch_ki,kdri_rao,init_age,diab,on_dialysis,est_rec_age_txp,est_rec_months_dial,gf
scaler = StandardScaler()
CSV_COLUMNS_FIRE = ("age_don","hgt_cm_don_calc","wgt_kg_don_calc","ethcat_don","hist_hypertens_don","hist_diabetes_don","cod_cad_don","creat_don","hep_c_anti_don","non_hrt_don","bmis","drmis","txkid","tx_procedur_ty_ki","cold_isch_ki","kdri_rao","init_age","diab","on_dialysis","est_rec_age_txp","est_rec_months_dial","gf")
input_reader = pd.read_csv(tf.gfile.Open('./organTXP.csv'), names=CSV_COLUMNS_FIRE, na_values='NA')
input_reader = input_reader.fillna(0)

# input_reader['tx_date'] = pd.to_datetime(input_reader['tx_date']).apply(lambda x: x.timestamp())

input_reader.hist_hypertens_don = pd.Categorical(input_reader.hist_hypertens_don)
input_reader['hist_hypertens_don'] = input_reader.hist_hypertens_don.cat.codes

input_reader.hep_c_anti_don = pd.Categorical(input_reader.hep_c_anti_don)
input_reader['hep_c_anti_don'] = input_reader.hep_c_anti_don.cat.codes

input_reader.non_hrt_don = pd.Categorical(input_reader.non_hrt_don)
input_reader['non_hrt_don'] = input_reader.non_hrt_don.cat.codes

input_reader.txkid = pd.Categorical(input_reader.txkid)
input_reader['txkid'] = input_reader.txkid.cat.codes

input_reader.on_dialysis = pd.Categorical(input_reader.on_dialysis)
input_reader['on_dialysis'] = input_reader.on_dialysis.cat.codes

# input_reader['init_date'] = pd.to_datetime(input_reader['init_date']).apply(lambda x: x.timestamp())

# attention too many NA on this feature, maybe trim this one out?
# input_reader['dialysis_date'] = pd.to_datetime(input_reader['dialysis_date']).apply(lambda x: x.timestamp())

# input_reader['dial_date'] = pd.to_datetime(input_reader['dial_date']).apply(lambda x: x.timestamp())

# input_reader['est_rec_dob'] = pd.to_datetime(input_reader['est_rec_dob']).apply(lambda x: x.timestamp())

y = input_reader['gf'].tolist()
x = input_reader[["age_don","hgt_cm_don_calc","wgt_kg_don_calc","ethcat_don","hist_hypertens_don","hist_diabetes_don","cod_cad_don","creat_don","hep_c_anti_don","non_hrt_don","bmis","drmis","txkid","tx_procedur_ty_ki","cold_isch_ki","kdri_rao","init_age","diab","on_dialysis","est_rec_age_txp","est_rec_months_dial"]].as_matrix()

seed = 21
test_size = 0.33
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

learning_rate = 0.01
model = Sequential()
model.add(Dense(1024, input_dim=21, activation='linear'))
model.add(Dense(580, activation='relu'))
model.add(Dense(1024, activation='sigmoid'))
model.add(Dense(580, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mse',
                optimizer='rmsprop',
                metrics=['accuracy'])

# model = Sequential()
# model.add(Conv2D(32, kernel_size=2, strides=1,
#         kernel_initializer="normal", 
#         padding="same",
#         input_dim=26))
# model.add(Activation("relu"))
# model.add(Conv2D(64, kernel_size=2, strides=1, 
#         kernel_initializer="normal", 
#         padding="same"))
# model.add(Activation("relu"))
# model.add(Conv2D(64, kernel_size=2, strides=1,
#         kernel_initializer="normal",
#         padding="same"))
# model.add(Activation("relu"))
# model.add(Flatten())
# model.add(Dense(512, kernel_initializer="normal"))
# model.add(Activation("relu"))
# model.add(Dense(3, kernel_initializer="normal"))

# model.compile(optimizer=Adam(lr=1e-6), loss="mse")

tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()))
print(x_train)
print(y_train)
history = model.fit(x_train, y_train, epochs=100, batch_size=100, verbose=1, callbacks=[tensorboard], shuffle=True)
model.test_on_batch(x_test, y_test)


scores = model.evaluate(x_test, y_test)
print(model.summary())
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
plot_model(model, to_file="plot.png", show_layer_names=True, show_shapes=True)

print(history.history.keys())
#  "Accuracy"
plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# "Loss"
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

# xg = XGBClassifier()
# xg.fit(x_train, y_train)
# predictions_xgb = xg.predict(x_test)
# print("Accuracy: %0.4f" % accuracy_score(y_test, predictions_xgb))

model.save('fire.h5')