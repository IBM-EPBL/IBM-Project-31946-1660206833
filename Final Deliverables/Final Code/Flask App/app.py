import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session

app=Flask(__name__)
model = load_model("vegetables.h5")
model1 = load_model("fruits.h5")
@app.route('/')
#home page
def home():
    return render_template('index.html')

#prediction page
@app.route('/prediction.html')
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        f=request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(128,128))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)
        plant=request.form['plants']
        print(plant)
        p = ""
        disease = ""
        caution = ""
        if(plant=="Vegetable"):
            y = np.argmax(model.predict(x),axis=1)     
            df = pd.read_excel('precautions - veg.xlsx')
            caution = df.iloc[y[0]]['caution']
            p = df.iloc[y[0]]['plant']
            disease = df.iloc[y[0]]['disease']
        else:
            y = np.argmax(model1.predict(x),axis=1)  
            df = pd.read_excel('precautions - fruits.xlsx')
            caution = df.iloc[y[0]]['caution']
            p = df.iloc[y[0]]['plant']
            disease = df.iloc[y[0]]['disease']
        if "healthy" in disease:
            str = "Prediction: Wow!! Your " + p + " plant is " + caution
            return str
        else:
            str = "Prediction: Oopps!! Your " + p + " plant is infected by " + disease + ". " + caution
            return str

if __name__ ==  "__main__":
    app.run(debug=False)  