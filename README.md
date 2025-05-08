# 🍎 FruitVision

**FruitVision** is an intelligent fruit recognition system that detects and classifies fruits from either camera snapshots or uploaded images. Built with **Django** and **TensorFlow**, it provides a user-friendly web interface for fruit identification using deep learning.

---

## 🚀 Features

- 🍌 Real-time fruit detection via camera
- 🍓 Upload image and predict fruit class
- 🔒 User authentication system (Sign Up / Login)
- 📊 Model visualization and prediction feedback
- 🌐 Clean and responsive web interface

---

## 🛠️ Prerequisites

Before running this project, ensure you have the following installed:
- numpy
- matplotlib
- seaborn
- pillow
- tensorflow
- django

## How to Run
1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/FruitVision.git
   cd FruitVision
   cd fruit_classifier/fruit_classifier

2. **Set Up Pipenv Environment:**
 - If you don’t have Pipenv installed:
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell

3. **Set Up Django Project:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

4. **Run The Server:**
   ```bash
   python manage.py runserver
- Go to http://127.0.0.1:8000/



