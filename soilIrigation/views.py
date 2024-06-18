# views.py
import threading
import time
from django.shortcuts import render, redirect
from .forms import SoilDataForm
from .models import IrrigationStatus
from .utils import predict_irrigation_from_random_data

from django.http import JsonResponse

def fetch_status(request):
    status = IrrigationStatus.objects.first()
    return JsonResponse({'status': status.status})

# Define a function to continuously predict irrigation status
def continuous_prediction(interval=1):
    while True:
        status, moisture, temperature = predict_irrigation_from_random_data()
        print(f"Status: {status}, Moisture: {moisture}, Temperature: {temperature}")
        IrrigationStatus.objects.update_or_create(id=1, defaults={'status': status})
        time.sleep(interval)

# Start the continuous prediction in a separate thread if not already started
continuous_prediction_thread = threading.Thread(target=continuous_prediction, daemon=True)


def soil_data_view(request):
    # form = SoilDataForm()
    continuous_prediction_thread.start()
    status = IrrigationStatus.objects.first()
    return render(request, 'soil_data_view.html', {"""'form': form,""" 'status': status})


def simulate_live_data(request):
    # Generate random data and predict irrigation status
    status, moisture, temperature = predict_irrigation_from_random_data()

    # Update the irrigation status in the database
    IrrigationStatus.objects.update_or_create(id=1, defaults={'status': status})

    # Render the template with the current status and random data
    return render(request, 'live_data_simulation.html', {
        'status': status,
        'moisture': moisture,
        'temperature': temperature,
    })
