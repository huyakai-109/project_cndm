import pandas as pd
import joblib

# Load the model and scaler
model = joblib.load('model.joblib')
scaler = joblib.load('scaler.joblib')

def input_features():
    # Manually input the feature data
    gender = input("Enter gender (0 for male, 1 for female): ")
    days_between = input("Enter days between scheduled day and appointment day: ")
    age = input("Enter age: ")
    scholarship = input("Scholarship (0 for no, 1 for yes): ")
    hypertension = input("Hypertension (0 for no, 1 for yes): ")
    diabetes = input("Diabetes (0 for no, 1 for yes): ")
    alcoholism = input("Alcoholism (0 for no, 1 for yes): ")
    handicap = input("Handicap level (0-4): ")

    # Create a DataFrame from the inputs
    data = pd.DataFrame({
        'Gender': [int(gender)],
        'DaysBetween': [int(days_between)],
        'Age': [int(age)],
        'Scholarship': [int(scholarship)],
        'Hipertension': [int(hypertension)],
        'Diabetes': [int(diabetes)],
        'Alcoholism': [int(alcoholism)],
        'Handcap': [int(handicap)]
    })

    return data

def predict_no_show(data, threshold=0.4):
    # Ensure the input is in the correct format (e.g., a DataFrame)
    data_scaled = scaler.transform(data)
    
    # Make probability prediction
    prediction_probs = model.predict_proba(data_scaled)[0]
    no_show_prob = prediction_probs[1]  # Probability of 'No-show'
    print(f"Probability of No-show: {no_show_prob}")
    
    # Make a prediction based on a threshold
    prediction = 1 if no_show_prob > threshold else 0
    return 'No-show' if prediction == 1 else 'Will show'


def main():
    print("Please enter the patient's details to predict no-show:")
    user_input_data = input_features()
    result = predict_no_show(user_input_data)
    print(f"The prediction is: {result}")
    
    # Check if an SMS needs to be sent
    if result == 'No-show':
        print("SMS should be sent to the patient due to predicted no-show.")

if __name__ == '__main__':
    main()
