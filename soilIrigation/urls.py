# soilapp/urls.py
from django.urls import path
from .views import soil_data_view
from soilIrigation import views

urlpatterns = [
    path('', soil_data_view, name='soil_data'),
     path('simulate/', views.simulate_live_data, name='simulate_live_data'),
     path('fetch_status/', views.fetch_status, name='fetch_status'),
]
