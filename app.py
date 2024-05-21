from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re
import pyttsx3
import csv
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
import numpy as np
from ocr import read_pdf 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

training = pd.read_csv('Training.csv')
testing = pd.read_csv('Testing.csv')
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
clf1 = DecisionTreeClassifier()
clf = clf1.fit(x_train, y_train)
model = SVC()
model.fit(x_train, y_train)

severityDictionary = {}
description_list = {}
precautionDictionary = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def read_severity_dict():
    global severityDictionary
    try:
        with open('symptom_severity.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) == 2:
                    severityDictionary[row[0]] = int(row[1])
    except Exception as e:
        print(f"Error reading severity dictionary: {e}")

def read_description_list():
    global description_list
    try:
        with open('symptom_Description.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) == 2:
                    description_list[row[0]] = row[1]
    except Exception as e:
        print(f"Error reading description list: {e}")

def read_precaution_dict():
    global precautionDictionary
    try:
        with open('symptom_precaution.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) == 5:
                    precautionDictionary[row[0]] = row[1:]
    except Exception as e:
        print(f"Error reading precaution dictionary: {e}")

read_severity_dict()
read_description_list()
read_precaution_dict()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text = read_pdf(file_path)  # Assuming read_pdf function is implemented
        return render_template('index.html', extracted_text=extracted_text)
    return redirect(request.url)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    symptom = request.form.get('symptom')
    days = int(request.form.get('days', 0))
    response = process_symptom(symptom, days)
    return jsonify(response)

def process_symptom(symptom, days):
    symptoms_dict = {symptom: index for index, symptom in enumerate(cols)}
    input_vector = np.zeros(len(symptoms_dict))
    if symptom in symptoms_dict:
        input_vector[symptoms_dict[symptom]] = 1

    disease_prediction = clf.predict([input_vector])[0]
    disease_name = le.inverse_transform([disease_prediction])[0]

    additional_info = {
        'severity': severityDictionary.get(symptom, 'Unknown'),
        'description': description_list.get(disease_name, 'No description available'),
        'precautions': precautionDictionary.get(disease_name, ['No precautions available'])
    }

    advice = "You should take the consultation from a doctor." if (severityDictionary.get(symptom, 0) * days) / (1 + 1) > 13 else "It might not be that bad but you should take precautions."

    return {
        'disease': disease_name,
        'additional_info': additional_info,
        'advice': advice
    }

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
