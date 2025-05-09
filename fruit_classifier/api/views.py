import base64
import pickle
from io import BytesIO
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import numpy as np
import seaborn as sns
from PIL import Image
from collections import defaultdict
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
import matplotlib.pyplot as plt

class_labels = ["Apple", "Banana", "Cherry", "Chickoo", "Grapes", 
                "Kiwi", "Mango", "Orange", "Strawberry"]

# MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'api', 'models', '1.h5')
# model = load_model(MODEL_PATH)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'api', 'fruits')
MODEL_PATH = os.path.join(BASE_DIR, 'api', 'models', '2.pkl')
MODEL_METRICS_PATH = os.path.join(BASE_DIR, 'api', 'models', 'metrics.pkl')

print(f"Loading model from: {MODEL_PATH}")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("Model Loaded Successfully") 

def home(request):
    return render(request, 'home.html')


@login_required(login_url=reverse_lazy('home'))
def dashboard_view(request):
    # 1. Dataset Stats
    class_counts = {}
    total_images = 0
    try:
        for class_name in os.listdir(DATASET_DIR):
            class_path = os.path.join(DATASET_DIR, class_name)
            if os.path.isdir(class_path):
                count = len([
                    f for f in os.listdir(class_path)
                    if f.lower().endswith(('.jpg', '.png', '.jpeg'))
                ])
                class_counts[class_name] = count
                total_images += count
    except Exception as e:
        print("Error loading dataset stats:", e)

    # 2. Load Model Metrics
    model_accuracy = None
    confusion_matrix = None
    try:
        with open(MODEL_METRICS_PATH, "rb") as f:
            metrics = pickle.load(f)
            confusion_matrix = metrics.get("confusion_matrix")
    except Exception as e:
        print("Error loading metrics:", e)

    # Chart 1: Bar chart of dataset distribution
    plt.figure(figsize=(8, 5))
    plt.bar(class_counts.keys(), class_counts.values(), color='skyblue')
    plt.title("Image Count per Fruit Class")
    plt.xlabel("Class")
    plt.ylabel("Number of Images")
    plt.tight_layout()
    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png')
    plt.close()
    bar_chart = base64.b64encode(buffer1.getvalue()).decode()

    # Chart 2: Confusion matrix (if available)
    confusion_matrix_img = None
    if confusion_matrix is not None:
        plt.figure(figsize=(6, 5))
        sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png')
        plt.close()
        confusion_matrix_img = base64.b64encode(buffer2.getvalue()).decode()

    return render(request, 'dashboard.html', {
        'class_counts': class_counts,
        'total_images': total_images,
        'num_classes': len(class_counts),
        
        'bar_chart': f'data:image/png;base64,{bar_chart}',
        'confusion_matrix_img': f'data:image/png;base64,{confusion_matrix_img}' if confusion_matrix_img else None,
    })



def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL  # Or '/'
    
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

@login_required(login_url=reverse_lazy('home'))
def predict(request):
    prediction = None
    image_base64 = None 

    if request.method == 'POST':
        print("POST request received")
        img = None
        
        # Handle file upload
        if 'image' in request.FILES:
            print("Image file received")
            image_file = request.FILES['image']
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = image_file.name.split('.')[-1].lower()
            
            if file_extension not in valid_extensions:
                return render(request, 'index.html', {
                    'error': 'Invalid file format. Please upload JPG, JPEG, or PNG images only.',
                    'prediction': None,
                    'image_base64': None
                })
                
            try:
                img = Image.open(image_file).convert("RGB")
                
                # Save for display
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                image_base64 = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"
            except Exception as e:
                return render(request, 'index.html', {
                    'error': 'Error processing the image file.',
                    'prediction': None,
                    'image_base64': None
                })
            
        # Handle camera image (data URL)
        elif 'image' in request.POST:
            print("Camera image received")
            data_url = request.POST['image']
            
            # Check if it's a supported image format
            if not data_url.startswith(('data:image/jpeg;base64', 'data:image/jpg;base64', 'data:image/png;base64')):
                return render(request, 'index.html', {
                    'error': 'Invalid image format. Please use JPG, JPEG, or PNG images only.',
                    'prediction': None,
                    'image_base64': None
                })
                
            try:
                header, data = data_url.split(',', 1)
                img_data = base64.b64decode(data)
                img = Image.open(BytesIO(img_data)).convert("RGB")
                
                # Save for display
                image_base64 = data_url
            except Exception as e:
                return render(request, 'index.html', {
                    'error': 'Error processing the camera image.',
                    'prediction': None,
                    'image_base64': None
                })
        
        # Process image for prediction
        if img:
            try:
                img = img.resize((224, 224)) 
                img_array = image.img_to_array(img) / 255.0 
                img_array = np.expand_dims(img_array, axis=0) 

                # Make prediction
                predictions = model.predict(img_array)
                predicted_index = np.argmax(predictions)
                predicted_label = class_labels[predicted_index]
                
                prediction = predicted_label
                print(f"Prediction: {prediction}")
            except Exception as e:
                return render(request, 'index.html', {
                    'error': 'Error during image processing or prediction.',
                    'prediction': None,
                    'image_base64': None
                })

    return render(request, 'index.html', {
        'prediction': prediction,
        'image_base64': image_base64,
        'error': None  # Explicitly set error to None when everything is fine
    })


@anonymous_required(redirect_url='home')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@anonymous_required(redirect_url='home')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


