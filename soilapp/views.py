from django.shortcuts import render, redirect
from .models import Profile, ChatMessage, SoilData  
from .forms import SignUpForm, SoilPropertiesForm, ChatForm
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import google.generativeai as palm
import os


# Create your views here.

def index(request):
    #profiles = Profile.objects.all()
    #soils = SoilData.objects.all()

    """
    context = {
        'profiles': profiles,
        'soils': soils,
    }
    """
    return render(request, 'index.html')

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    """Login an existing user."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': form})

def logout_view(request):
    """Logout an existing user."""
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

@login_required(login_url='login')
def soil_data(request):
    """Add a new soil data entry."""
    if request.method == 'POST':
        form = SoilDataForm(request.POST)
        if form.is_valid():
            try:
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return redirect('user_dashboard')
            except Exception as e:
                return render(request, 'soil_data.html', {'form': form, 'error': e})
        else:
            return render(request, 'soil_data.html', {'form': form, 'error_message': 'Form validation failed.'})
    else:
        form = SoilDataForm()
    return render(request, 'soil_data.html', {'form': form})

@login_required(login_url='login')
def user_dashboard(request):
    # Fetch authenticated user's soil data from your database
    soil_data = SoilData.objects.filter(user=request.user)
    # Implement logic to calculate health assessments
    return render(request, 'user_dashboard.html', {'soil_data': soil_data})


@login_required(login_url='login')
def soil_properties_analysis(request):
    """Add a new soil properties analysis."""
    if request.method == 'POST':
        palm.configure(api_key=os.environ['PALM_API_KEY'])
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        model = models[0].name
        form = SoilPropertiesForm(request.POST)
        if form.is_valid():
            # Create a list of user-supplied properties
            user_properties = []

            # Iterate through the form.cleaned_data dictionary
            for field_name, field_value in form.cleaned_data.items():
                if field_value:
                    user_properties.append(f"{form.fields[field_name].label}: {field_value}")

            # Construct the prompt using user-supplied properties
            prompt = "Please analyze the soil with the following properties:\n\n" + "\n".join(user_properties) + "\n\n" + "Based on these properties, analyze the soil quality, identify any potential issues, and provide detailed recommendations for improving the soil conditions. Consider factors like nutrient deficiencies, pH adjustments, and specific agronomic practices that can optimize soil health and crop yield. Your expertise is invaluable in helping our users make informed decisions for their farming and gardening endeavors."

            # Use the text completion model to generate a response
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0.7,  # Adjust temperature as needed
                max_output_tokens=800,  # Adjust max length as needed
            )

            # Get the generated response from the completion
            generated_response = completion.result

            return render(request, 'analysis_result.html', {'generated_response': generated_response})

    else:
        form = SoilPropertiesForm()

    return render(request, 'soil_properties_input_form.html', {'form': form})





@login_required(login_url='login')
def chat_view(request):
    """Add a new chat message."""
    if request.method == 'POST':
        palm.configure(api_key=os.environ['PALM_API_KEY'])
        form = ChatForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            if prompt == 'quit':
                return redirect('chat_view')  # Redirect to chat view when 'quit' is entered

            # Use your chat model here to generate a response
            response = palm.chat(
                context="Be a professional soil scientist with vast and accurate knowledge in soil science, agronomy, and general agriculture.",
                examples=[],
                messages=prompt
            )

            # Get the username of the current user
            user = request.user

            # Save the user's input and the model's response to your database
            ChatMessage.objects.create(user=user, user_input=prompt, model_response=response.last)
    else:
        form = ChatForm()

    # Fetch all chat messages from your database
    chat_messages = ChatMessage.objects.filter(user=request.user)

    return render(request, 'chat_page.html', {'form': form, 'chat_messages': chat_messages})

# RYEKO AI ryeko.org

