import pickle, bz2
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from app_logger import *
import warnings
import logging
from logging import Formatter, FileHandler
warnings.filterwarnings("ignore")


app = Flask(__name__)

# Import Classification and Regression model file
C_pickle = bz2.BZ2File('saved_dt_model.pkl', 'rb')
model_C = pickle.load(C_pickle)



# Route for homepage
@app.route('/')
def home():
    log.info('Home page loaded successfully')
    return render_template('index.html')



# Route for Classification Model

@app.route('/predictC', methods=['POST', 'GET'])
def predictC():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Temperature=float(request.form['Temperature'])
            Wind_Speed =int(request.form['Ws'])
            FFMC=float(request.form['FFMC'])
            DMC=float(request.form['DMC'])
            ISI=float(request.form['ISI'])

            features = [Temperature, Wind_Speed,FFMC, DMC, ISI]

            Float_features = [float(x) for x in features]
            final_features = [np.array(Float_features)]
            prediction = model_C.predict(final_features)[0]

            log.info('Prediction done for Classification model')

            if prediction == 0:
                text = 'Forest is Safe!'
            else:
                text = 'Forest is in Danger!'
            return render_template('index.html', prediction_text1="{} --- Chance of Fire is {}".format(text, prediction))
        except Exception as e:
            log.error('Input error, check input', e)
        return render_template('index.html', prediction_text1="Check the Input again!!!")