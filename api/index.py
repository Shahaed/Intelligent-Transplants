from keras.models import load_model
from flask import Flask
import numpy as np
app = Flask(__name__)

model = load_model('./transplant.h5')

@app.route("/")
def main():
    return "hello<br><br><br><br>how are you?"

@app.route("/<dr>/<age>/<blood>/<gender>/<ethnicity>/<bmi>/<lod>")
def ml_decision(dr, age, blood, gender, ethnicity, bmi, lod):
    print('you called ml_prediction route')
    input = [float(dr), float(age), float(blood), float(gender), float(ethnicity), float(bmi), float(lod)]
    input = np.reshape(input, (1, 7))
    output = model.predict(input)
    print(str(output[0][0]))
    return str(output[0][0])