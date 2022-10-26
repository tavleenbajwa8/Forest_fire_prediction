import pickle
#from typing_extensions import TypeVarTuple
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from app_logger import log
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)

# Import Classification and Regression model file

#model_C = pd.read_pickle(r'saved_dt_model1.pkl')
C_pickle = open("saved_dt_model.pkl",'rb')
model_C = pickle.load(C_pickle)

# with open pickle.load('saved_dt_model.pkl', 'rb') as model_C:
#     model_C = pickle.load(C_pickle)
# C_pickle = bz2.BZ2File('saved_dt_model.bz2', 'rb')
# model_C = pickle.load(C_pickle)



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


# Run APP in Debug mode
if __name__ == "__main__":
    app.run(debug=True, port= 5000)