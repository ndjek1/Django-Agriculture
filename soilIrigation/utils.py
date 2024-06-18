# soilapp/utils.py
import pickle
import os
import random
from .models import SoilData

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'irrigation_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict_irrigation_from_random_data():
    # Generate random soil data
    moisture = random.uniform(0, 100)  # Example range for moisture
    temperature = random.uniform(0, 40)  # Example range for temperature

    # Convert to the format expected by the model
    features = [moisture, temperature]

    # Make a prediction
    prediction = model.predict([features])[0]

    # Return the prediction and the random data
    return prediction == 1, moisture, temperature
