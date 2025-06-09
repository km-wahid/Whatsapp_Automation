import os
import csv
from pyexpat.errors import messages
import random
import requests
import shutil
import platform
import time
import subprocess
import urllib.parse
import pandas as pd
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.core.files.storage import FileSystemStorage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from django.utils.timezone import now
from Whatsapp import settings
from .models import WhatsAppNumber , CSVFile, Template, UserSession,MessageHistory, SenderID
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .forms import TemplateForm
from django.http import JsonResponse, HttpResponseBadRequest
from web.tasks import send_whatsapp_message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'web/login.html', {'form': form, 'title': 'Login'})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
# This function will take the homepage
def dashboard(request):
    total_users = UserSession.objects.count()  # Total number of users
    total_profiles = UserSession.objects.values("profile_path").distinct().count()  # Unique profile paths

    context = {
        "total_users": total_users,
        "total_profiles": total_profiles
    }
    return render(request, "web/dashboard.html", context)

@login_required
#Users upload csv's this function take resposible for takeing this is .csv file or not then it go for process
def upload_csv(request):
    """
    Handles CSV file upload, saves it to the database, and processes it.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Save the CSV file in the database
        csv_entry = CSVFile.objects.create(file=csv_file)

        # Ensure the file is saved before processing
        csv_entry.refresh_from_db()  
        csv_path = csv_entry.file.path

        # Process the CSV file
        process_csv_file(csv_path)

        return redirect('create_template')  # Redirect after successful upload

    return render(request, 'web/upload.html')


def process_csv_file(file_path):
    """
    Reads and processes the CSV file, saving valid numbers to the database.
    """
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        # WhatsAppNumber.objects.all().delete()  # Clears previous data
        
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensure the row is not empty
                    number = row[0].strip()
                    if number.isdigit():  # Validate phone number format
                        WhatsAppNumber.objects.get_or_create(number=number)

        print("CSV File processed successfully")
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")



@login_required
def campaign_view(request):
    """Handles message sending request"""
    if request.method == 'POST':
        template_id = request.POST.get('template')
        csv_file_id = request.POST.get('csv_file')
        user_id = request.POST.get('user')

        if not template_id or not csv_file_id or not user_id:
            return HttpResponse("Please select a template, CSV file, and user session.", status=400)

        template = get_object_or_404(Template, id=template_id)
        csv_instance = get_object_or_404(CSVFile, id=csv_file_id)
        user_session = get_object_or_404(UserSession, id=user_id)

       
        phone_numbers = []
        try:
            with open(csv_instance.file.path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                phone_numbers = [row[0].strip() for row in reader if row]
        except Exception as e:
            return HttpResponse(f"Error processing CSV file: {str(e)}", status=500)

        # Queue task for background processing
        send_whatsapp_message.delay(phone_numbers, template.message, user_session.profile_path)
        # send_whatsapp_message(phone_numbers, template.message, user_session.profile_path)

        return render(request, 'web/success.html')  

    templates = Template.objects.all()
    csv_files = CSVFile.objects.all()
    user_sessions = UserSession.objects.all()

    return render(request, 'web/camp.html', {
        'templates': templates,
        'csv_files': csv_files,
        'user_sessions': user_sessions
    })

    # Fetch all templates, CSV files, and user sessions
    templates = Template.objects.all()
    csv_files = CSVFile.objects.all()
    user_sessions = UserSession.objects.all()

    return render(request, 'web/camp.html', {
        'templates': templates,
        'csv_files': csv_files,
        'user_sessions': user_sessions,
        'message': message,
    })



# Template input from user
@login_required
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('campaign_view') 
            
    else:
        form = TemplateForm()
        
        
    

    return render(request, 'web/create_template.html', {'form': form})




    # return render(request, 'web/create_template.html', {'form': form})



@login_required
def user_list(request):
    """Retrieve all active WhatsApp sessions and display them."""
    users = UserSession.objects.all()  # Get all users from the database
    return render(request, 'web/user_list.html', {'users': users})  # Pass users to the template




# Path to Chrome executable 

CHROME_EXECUTABLE = get_chrome_executable()



# Directory where user profiles will be stored
CHROME_USER_DATA_PATH = os.path.join(settings.BASE_DIR, 'chrome_profiles')



def get_chrome_executable():
    import shutil, os, platform

    system = platform.system()

    common_paths = {
        'Linux': [
            'google-chrome',
            'google-chrome-stable',
            'chromium-browser',
            'chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
        ],
        'Darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ],
        'Windows': [
            'chrome.exe',
        ],
    }

    for name in common_paths.get(system, []):
        path = shutil.which(name) if not name.startswith('/') else name
        if path and os.path.exists(path):
            return path

    raise EnvironmentError("Chrome executable not found.")



def process_and_send_messages(user_name):
    """Fetch user message, retrieve CSV, extract numbers, and send messages."""
    try:
        user_session = UserSession.objects.get(user_name=user_name)
        sender_profile = user_session.profile_path

        df = pd.read_csv(user_session.csv_file.path)
        phone_numbers = df['phone'].astype(str).tolist()

        send_whatsapp_message(phone_numbers, user_session.message, sender_profile)

    except Exception as e:
        print(f"Error: {e}")



















def create_chrome_profile(user_name):
    """Creates a unique Chrome profile directory for the user."""
    profile_path = os.path.join(CHROME_USER_DATA_PATH, user_name)
    
    # Ensure the profile directory exists
    os.makedirs(profile_path, exist_ok=True)
    
    return profile_path  







def open_whatsapp_in_chrome(profile_path):
    """Open WhatsApp Web in headless Chrome with a user-specific profile."""
    
    whatsapp_url = 'https://web.whatsapp.com'
    chrome_executable = get_chrome_executable()

    try:
        subprocess.Popen([
            chrome_executable,
            f'--user-data-dir={profile_path}',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-default-apps',
            '--disable-features=SigninIntercept,SignInProfileCreation',
            '--disable-sync',
            '--disable-extensions',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-client-side-phishing-detection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--metrics-recording-only',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--mute-audio',
            '--window-size=1920,1080',
            '--headless=new',  # Use --headless=new for newer Chrome versions
            whatsapp_url
        ])
        time.sleep(10)  # Let Chrome load
    except Exception as e:
        print(f"Error launching headless Chrome: {e}")
        return HttpResponse(f"Error opening WhatsApp Web: {e}", status=500)

    


@login_required
def create_whatsapp_session(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')

        if not user_name:
            return HttpResponse("Phone number is required.", status=400)

        # if UserSession.objects.count() >= 10:
        #     return HttpResponse("Maximum number of sender IDs reached.", status=400)

        if UserSession.objects.filter(user_name=user_name).exists():
            return HttpResponse("This sender ID already exists.", status=400)

        profile_path = create_chrome_profile(user_name)
        new_session = UserSession.objects.create(user_name=user_name, profile_path=profile_path)
        SenderID.objects.create(user_session=new_session)

        # open_whatsapp_in_chrome(profile_path)
        return login_qr(request)

        # return redirect('upload_csv')  # or wherever your next step is

    return render(request, 'web/wa_login.html')




@login_required
def history(request):
    """View to display all message history."""
    # message_history = MessageHistory.objects.select_related('user', 'template').order_by('-sent_time')

    # return render(request, 'web/history.html', {'message_history': message_history})
    return render(request, 'web/history.html',)
    pass


@login_required
def api_docs(request):
    return render(request, 'web/api_docs.html')








@login_required


def login_qr(request):
    return render(request, "web/login_qr.html")






import requests
from django.http import JsonResponse

def proxy_qr_json(request):
    try:
        res = requests.get("http://localhost:3001/qr-json", timeout=5)
        return JsonResponse(res.json())
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_login_success(user_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"qr_login_{user_id}",
        {
            'type': 'login_successful',
        }
  )
