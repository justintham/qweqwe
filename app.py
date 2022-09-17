# from pyexpat import model
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
# import os
# import sendgrid
# import requests
# from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

# 

def get_algorithm(x):
    x=int(x)
    if x == 0:
        model = pickle.load(open('algorithm/model_rf.pkl', 'rb'))
    elif x == 1:
        model = pickle.load(open('algorithm/model_gb.pkl', 'rb'))
    elif x == 2:
        model = pickle.load(open('algorithm/model_knn.pkl', 'rb'))
    elif x == 3:
        model = pickle.load(open('algorithm/model_svm.pkl', 'rb'))
    elif x == 4:
        model = pickle.load(open('algorithm/model_dt.pkl', 'rb'))
    elif x == 5:
        model = pickle.load(open('algorithm/model_log.pkl', 'rb'))
    elif x == 6:
        model = pickle.load(open('algorithm/model_gnb.pkl', 'rb'))
    return model

# def send_email(email):
#     message = Mail(
#         from_email='hesheitaliabu@gmail.com',
#         to_emails=email,
#         subject='testing 123',
#         html_content='<strong>testing 123</strong>')
#     Sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('MyAPI'))
#     Sg.send(message)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# @app.route("/login_page", methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')

@app.route("/login_page", methods=['GET', 'POST'])
def login():
    # if request.method == "POST":
    #     email = request.form.get("email")
    #     # data =  { 'Name': email}
    #     # firebase.post('/python-example-f6d0b/Students/',data)
    #     # return redirect(f"/success/{email}")
    #     # return render_template('main.html')
    return render_template('login.html')

    
# @app.route('/success/<email>')
# def success(email):
#     send_email(email)
#     return render_template('main.html')

@app.route("/about_us_page", methods=['GET', 'POST'])
def about_us():
    return render_template('about_us.html')

@app.route("/signup_page", methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route("/predict_page", methods=['GET', 'POST'])
def predict_page():
    # redirect(url_for('success'))
    return render_template('main.html')


@app.route("/graph_page", methods=['GET', 'POST'])
def graph_page():
    return render_template('graph.html')

@app.route('/predict',methods=['GET', 'POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    age = request.form.get("age")
    sex = request.form.get("sex")
    cp = request.form.get("cp")
    trestbps = request.form.get("trestbps")
    chol = request.form.get("chol")
    fbs = request.form.get("fbs")
    restecg = request.form.get("restecg")
    thalach = request.form.get("thalach")
    oldpeak = request.form.get("oldpeak")
    exang = request.form.get("exang")
    slope = request.form.get("slope")
    ca = request.form.get("ca")
    thal = request.form.get("thal")
    algorithm = request.form.get("algorithm")
    data = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
    data = list(np.float_(data))
    result = get_algorithm(algorithm)
    scaler2 = StandardScaler()
    ##CHANGE THE INPUT TO NUMPY ARRAY
    input_data_as_numpy_array = np.asarray(data)
    #RESHAPE THE NUMPY ARRAY BECAUSE WE NEED TO PREDICT THE TARGET
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    std_data = scaler2.fit_transform(input_data_reshaped)
    prediction = result.predict(input_data_reshaped)
    if prediction[0] == 0:
        return render_template('main.html', prediction_text='The patient does not have Heart Disease' )
    else:
        return render_template('main.html', prediction_text='The patient has Heart Disease' )



if __name__ == "__main__":
    app.run(debug=True)