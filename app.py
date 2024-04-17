from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
from werkzeug.utils import secure_filename
import io
import numpy as np
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the model and scaler
model = joblib.load('model.joblib')
scaler = joblib.load('scaler.joblib')

@app.route('/predict', methods=['POST'])
def predict_no_show():
    # Get JSON data from POST request
    data = request.json
    # Convert JSON data to DataFrame
    input_data = pd.DataFrame({
        'Gender': [data['Gender']],
        'DaysBetween': [data['DaysBetween']],
        'Age': [data['Age']],
        'Scholarship': [data['Scholarship']],
        'Hipertension': [data['Hipertension']],
        'Diabetes': [data['Diabetes']],
        'Alcoholism': [data['Alcoholism']],
        'Handcap': [data['Handcap']]
    })
    # Scale the data
    data_scaled = scaler.transform(input_data)
    
    # Make probability prediction
    prediction_probs = model.predict_proba(data_scaled)[0]
    no_show_prob = prediction_probs[1]  # Probability of 'No-show'
    
    # Make a prediction based on a threshold
    threshold = 0.3
    prediction = 'No-show' if no_show_prob > threshold else 'Will show'

    # Return prediction result as JSON
    return jsonify({
        'probability': no_show_prob,
        'prediction': prediction
    })


# Route for Excel file prediction
@app.route('/predict_excel', methods=['POST'])
def predict_excel():
    if 'excelFile' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    file = request.files['excelFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        data = pd.read_excel(filepath)
        
        # Check for the presence of categorical columns and process them
        if 'Gender' in data.columns:
            data['Gender'] = data['Gender'].map({'F': 1, 'M': 0})
        else:
            data['Gender'] = 0  # Default value if Gender column is missing

        # Make sure other categorical columns are also converted

        # Exclude non-numeric columns from scaling
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        data_scaled = scaler.transform(data[numeric_cols])
        
        # Make predictions
        prediction_probs = model.predict_proba(data_scaled)[:, 1]
        data['No-show Prediction'] = np.where(prediction_probs > 0.3, 'No Show', 'Will Show')
        
        # Convert to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
        output.seek(0)

        # Send the Excel file as a response
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='predictions.xlsx'
        )

    except Exception as e:
        app.logger.error('Unhandled Exception: %s', (str(e)))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
