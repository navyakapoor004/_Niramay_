from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import SignUpForm,loginforms
from django.contrib import messages
import random
from .models import OTP
from django.core.mail import send_mail
from .models import customuser


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)  # Log in the user after sign-up
            return redirect("home")  # Redirect to home page
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form=loginforms(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                otp=generate_otp()
                OTP.objects.create(user=user, otp_code=otp)
                send_otp(user,otp)
                request.session['user_id'] = user.id
                return redirect('verify_otp')
            else:
                messages.error(request,'Invalid username or Password')
                return render(request,'accounts/login.html',{'forms':form})
        else:
            messages.error(request,'There was an error in the form. Please check the details.')
            return redirect('login')
    else:
        form=loginforms()
        return render(request,'accounts/login.html',{'forms': form})

def generate_otp():
    otp=str(random.randint(000000,999999))
    return otp
def send_otp(user,otp):
    subject="OTP"
    txt=f"your otp is {otp}"

    send_mail(subject,txt,'niramay0412@gmail.com',[user.email]

    )



def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST['otp_code']
        user_id = request.session.get('user_id')

        if user_id:
            try:
                user = customuser.objects.get(id=user_id)  # Fetch the custom user model
                otp_entry = OTP.objects.filter(user=user).latest('created_at')  # Get the latest OTP

                # Check if OTP is expired
                ### return redirect('login')  # Redirect to login if OTP expired

                # Validate OTP code
                if otp_entry.otp_code == otp_code:
                    login(request, user)  # Log the user in
                    messages.success(request, "Login successful")
                    return redirect('home')  # Redirect to home page or dashboard

                else:
                    messages.error(request, "Invalid OTP")
                    return render(request, 'accounts/verify_otp.html')

            except OTP.DoesNotExist:
                messages.error(request, "OTP not found for this user.")
                return redirect('login')

    return render(request, 'accounts/verify_otp.html')

def logout_page(request):
    logout(request)
    return redirect('home')