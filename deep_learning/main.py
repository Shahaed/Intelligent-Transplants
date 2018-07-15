from numpy import loadtxt
import numpy
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import time
import datetime
from sklearn.svm import SVC
from xgboost import XGBClassifier
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import TensorBoard
from keras.layers.core import Activation, Flatten
from keras.layers.convolutional import Conv2D
import h5py
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from keras import backend as K
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
# "tx_date","age_don","hgt_cm_don_calc","wgt_kg_don_calc","ethcat_don","hist_hypertens_don","hist_diabetes_don","cod_cad_don","creat_don","hep_c_anti_don","non_hrt_don","bmis","drmis","txkid","tx_procedur_ty_ki","cold_isch_ki","kdri_rao","init_age","init_date","diab","dialysis_date","on_dialysis","dial_date","est_rec_dob","est_rec_age_txp","est_rec_months_dial","gf"
import pandas as pd
import tensorflow as tf
from keras.models import load_model

scaler = StandardScaler()
CSV_COLUMNS_FIRE = ("tx_date","age_don","hgt_cm_don_calc","wgt_kg_don_calc","ethcat_don","hist_hypertens_don","hist_diabetes_don","cod_cad_don","creat_don","hep_c_anti_don","non_hrt_don","bmis","drmis","txkid","tx_procedur_ty_ki","cold_isch_ki","kdri_rao","init_age","init_date","diab","dialysis_date","on_dialysis","dial_date","est_rec_dob","est_rec_age_txp","est_rec_months_dial","gf")
input_reader = pd.read_csv(tf.gfile.Open('./organTXP.csv'), names=CSV_COLUMNS_FIRE, na_values='NA')
input_reader = input_reader.fillna(0)


input_reader['tx_date'] = pd.to_datetime(input_reader['tx_date']).apply(lambda x: x.timestamp())

input_reader.hist_hypertens_don = pd.Categorical(input_reader.hist_hypertens_don)
input_reader['hist_hypertens_don'] = input_reader.hist_hypertens_don.cat.codes

input_reader.hist_diabetes_don = pd.Categorical(input_reader.hist_diabetes_don)
input_reader['hist_diabetes_don'] = input_reader.hist_diabetes_don.cat.codes

input_reader.hep_c_anti_don = pd.Categorical(input_reader.hep_c_anti_don)
input_reader['hep_c_anti_don'] = input_reader.hep_c_anti_don.cat.codes

input_reader.non_hrt_don = pd.Categorical(input_reader.non_hrt_don)
input_reader['non_hrt_don'] = input_reader.non_hrt_don.cat.codes

input_reader.txkid = pd.Categorical(input_reader.txkid)
input_reader['txkid'] = input_reader.txkid.cat.codes

input_reader.on_dialysis = pd.Categorical(input_reader.on_dialysis)
input_reader['on_dialysis'] = input_reader.on_dialysis.cat.codes

input_reader['init_date'] = pd.to_datetime(input_reader['init_date']).apply(lambda x: x.timestamp())

# attention too many NA on this feature, maybe trim this one out?
input_reader['dialysis_date'] = pd.to_datetime(input_reader['dialysis_date']).apply(lambda x: x.timestamp())

input_reader['dial_date'] = pd.to_datetime(input_reader['dial_date']).apply(lambda x: x.timestamp())

input_reader['est_rec_dob'] = pd.to_datetime(input_reader['est_rec_dob']).apply(lambda x: x.timestamp())

y = input_reader['gf'].tolist()
x = input_reader[["tx_date","age_don","hgt_cm_don_calc","wgt_kg_don_calc","ethcat_don","hist_hypertens_don","hist_diabetes_don","cod_cad_don","creat_don","hep_c_anti_don","non_hrt_don","bmis","drmis","txkid","tx_procedur_ty_ki","cold_isch_ki","kdri_rao","init_age","init_date","diab","dialysis_date","on_dialysis","dial_date","est_rec_dob","est_rec_age_txp","est_rec_months_dial"]].as_matrix()

# print("shape of x is", x.shape)
# print('shape of y is', y.shape)

print('one row of x is', x[0])
print('one output of y is', y[0])

# print(x)
# print(y)
seed = 21
numpy.random.seed(seed)
test_size = 0.33
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=seed)

learning_rate = 0.01
model = Sequential()
model.add(Dense(1024, input_dim=21, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1024, activation='softmax'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
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
model.fit(x_train, y_train, epochs=1000, batch_size=1024, verbose=1, callbacks=[tensorboard])

scores = model.evaluate(x_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

x_test[0]

svm = SVC(probability=False, kernel='rbf', C=2,  gamma=.0073)
svm.fit(x_train, y_train)
predicted = svm.predict(x_test)
print("Accuracy: %0.4f" % accuracy_score(y_test,predicted))

xg = XGBClassifier()
xg.fit(x_train, y_train)
predictions_xgb = xg.predict(x_test)
print("Accuracy: %0.4f" % accuracy_score(y_test, predictions_xgb))

model.save('fire.h5')