
import threading
from django.shortcuts import render,HttpResponse,redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User as custonUser
from django.urls import reverse
from django.http import StreamingHttpResponse

from django.http import JsonResponse 
from .forms import VideoForm
from .models import Video
from ultralytics import YOLO

import uuid
import time

import cv2 
import random
import numpy as np 
import os

import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# from .forms import CustomUserCreationForm

model = YOLO('runs/classify/train1/weights/best.pt')
 
load_video_id = None
max_prob_name = ''
max_prob_value = ''
screenshot_paths = []
screenshot_names = []
values = []

mail_id=''

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    print('inside the home page ')
    clear_data(request)
    if request.method == 'POST':
        print('got the post request')
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = Video(name=form.cleaned_data['name'], video_file=form.cleaned_data['video_file'])
            video.save()
            return DetectAnomaly(request, video_id=video.id)
        # redirect('DetectAnomaly', video_id=video.id)
        else:
            print('Invalid')
    else:
        form = VideoForm()

    context = {
        'user': request.user,
        'form': form,
        'random_name': random.randint(0, 300)
        }
    return render (request,'home.html', context)

def clear_data(request): 
    global max_prob_name, max_prob_value , screenshot_paths,screenshot_names 
    max_prob_name = ''
    max_prob_value = ''
    screenshot_paths = []
    screenshot_names = []
    
    return 
    



def send_email():
    mail_id
    # Email details 'vidhaidigitalvidhika@gmail.com'
    sender_email = 'zeehanrashid1@gmail.com'
    sender_password ='vjhrjnfmwvixkrhf'
    receiver_email = mail_id
    subject = "Anomaly Detected"
    
    # Get the last saved screenshot
    last_screenshot = screenshot_paths[-1]
    
    # Create message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    # Attach the last screenshot to the message
    with open(last_screenshot, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype = "jpg")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(last_screenshot))
        message.attach(attachment)

    # Send the message
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender_email, sender_password)
        smtpObj.sendmail(sender_email, receiver_email, message.as_string())
        smtpObj.quit()
        return
    except Exception as e:
        print("Error sending email:", e)
        return





def screenshot_list(request):
    global screenshot_paths, screenshot_names
    return JsonResponse({'screenshot_paths': screenshot_paths , 'screenshot_names': screenshot_names})

def save_frames(frame, name):
    global screenshot_paths, screenshot_names
    directory = 'media/screenshot'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = str(uuid.uuid4()) + '.jpg'
    filepath = os.path.join(directory, filename)
    screenshot_paths.append(filepath)
    screenshot_names.append(name)
    with open(filepath, 'wb') as f:
        f.write(frame)
    # Run send_email function in a separate thread
    email_thread = threading.Thread(target=send_email)
    email_thread.start()


class VideoCapture:
    
    def __init__(self, device=0):
        self.cap = cv2.VideoCapture(device)
        if not self.cap.isOpened():
            raise ValueError("Unable to open camera/video")
        self.last_screenshot_time = time.time()

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        global max_prob_name, max_prob_value, values
        ret, frame = self.cap.read()
        if load_video_id == None: 
            frame = cv2.flip(frame, 1)
        
        current_time = time.time()
        elapsed_time = current_time - self.last_screenshot_time

        frame = model(frame)
        
        name = frame[0].names
        probs = frame[0].probs.tolist()
        max_prob_name = name[np.argmax(probs)]
        max_prob_value = max(probs)
        
        frame = frame[0].orig_img

        print('prob :  ', probs)
        # print('Max Prob Name:', max_prob_name )
        # print('Max Prob Value:', max_prob_value )
        

        if not ret:
            return None
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        if elapsed_time >= 0.6:
            self.last_screenshot_time = current_time
            if max_prob_name == 'non_violence' and  max_prob_value > 0.7: 
                values.append(max_prob_value)
                # max_prob_name = 'violence'
                if values and len(values) > 1  :
                    save_frames(frame, 'Anomaly')
            if max_prob_name == 'violence' and  max_prob_value > 0.5: 
                values = []

        # if elapsed_time >= 0.3:
        #     self.last_screenshot_time = current_time
        #     if max_prob_name == 'violence' and  max_prob_value > 0.88: 
        #         max_prob_name = 'violence'
        #         save_frames(frame, max_prob_name)
        return frame



def video_feed(request):
    if load_video_id == None:
        try:
            # Try to open camera 0
            cap = VideoCapture(0)
        except ValueError:
            # If camera 0 is not available, try to open camera 1
            cap = VideoCapture(1) 
    else: 
        try:
            # Try to open camera 0
            cap = VideoCapture(load_video_id)
        except ValueError:
            # If video is not available, print the error
            print('got error: ', ValueError) 

    def gen():
        while True:
            frame = cap.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def DetectAnomaly(request, video_id = None):
    global load_video_id, mail_id
    mail_id = request.user.e_email
    openCam = request.GET.get('openCam', '')

    if openCam == 'true':
        load_video_id = None
    else:
        video = get_object_or_404(Video, id=video_id)
        load_video_id = video.video_file.path

    data =  reverse('video_feed')

    
    context = {
        'video_feed_url': data, 
        'user': request.user
    }

    return render (request,'detect_anomaly.html', context)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)



# @login_required
def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    
    if request.method=='POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        e_email=request.POST.get('e_email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and conform password are not Same!!")
        else:
            # form = CustomUserCreationForm(username=uname, email=email, password=pass1, e_email=e_email)
            # form.save()
            
            my_user = custonUser.objects.create_user(name=name, email=email, e_email=e_email, password=pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')


# @login_required
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=email,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentails")
            # messages.warning(request,"Password is Incorrect")
            return redirect('/login') 
        
            # # Add an error message to the context if authentication fails
            # context = {'error_message': 'Invalid login credentials'}
            # return render(request, 'login.html', context)

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')



 
    