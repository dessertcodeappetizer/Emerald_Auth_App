from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User_auth
from django.contrib import messages
from .forms import MyUserCreationForm
from django.core.mail import send_mail
from AuthV1.settings import EMAIL_HOST_USER
import random, time
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
#login#
#############################################################
# @csrf_exempt
def loginPage(request):
    if request.user.is_authenticated:
        return render(request, 'welcome.html')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User_auth.objects.get(email=email)
        except:
            messages.error(request, "User not found")
        user = authenticate(request, email=email, password=password)
        print(user)
        nme = User_auth.objects.values('username').get(email=email)
        if user is not None:
            login(request, user)
            return render(request, 'welcome.html', {'username': nme})
        else:
            messages.error(request, "Email or Password doesnot exist")
    return render(request, 'login.html')

#logout
################################################################
def logoutUser(request):
    logout(request)
    return render(request, 'homepage.html')

#home
################################################################
def hp(request):
    return render(request, 'homepage.html')

#Send OTP
################################################################
ot = None
data_send_frntnd = None
# @csrf_exempt
def emailVerification(request):
    global ot
    global data_send_frntnd
    if request.method == 'POST':
        eml = request.POST.get('email')
        if eml is not None:
            exists = User_auth.objects.filter(email=eml).exists()
            if exists == True:
                messages.error(request, f"{eml} already exists")
                return redirect('login')
            data_send_frntnd = {'email': eml}
            ot = random.randint(100000, 999999)
            send_mail("Believe in Emerald: ", f"Greetings from Emerald, Your email verification OTP: /n {ot}", EMAIL_HOST_USER, [eml])
            messages.success(request, f"OTP sent to {eml}")
            return render(request, 'everify2.html')
        vrfy = request.POST.get('otp')
        if vrfy is not None:
            if ot == int(vrfy):
                return redirect('signup')
            else:
                messages.error(request, 'Please enter the correct OTP')
                return render(request, 'everify2.html')
    return render(request, 'everify1.html')

#signup
################################################################
# @csrf_exempt
def signupUser(request):
    if request.method == 'POST':
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if (pass1 != pass2):
            messages.error(request, 'Passwords do not match')
        else:
            form = MyUserCreationForm(request.POST)
            print(form)
            if form.is_valid():
                print("yes")
                user = form.save()
                user.save()
                print(user)
                
                login(request, user)
                return render(request, 'welcome.html')
            else:
                password2_errors = form.errors.get('password2', None)
                messages.error(request, password2_errors)
    return render(request, 'signup.html', context=data_send_frntnd)

#Forgot Password
########################################################################
ot1 = None
id1 = None
# @csrf_exempt
def forgotPassword(request):
    global ot1, id1
    if request.method == 'POST':
        eml1 = request.POST.get('email')
        if eml1 is not None:
            val_exists = User_auth.objects.filter(email=eml1).exists()
            if val_exists == False:
                messages.error(request, "Email does not exist!")
                return redirect('login')
            else:
                ied = User_auth.objects.values('id').get(email=eml1)
                id1 = ied['id']
                ot1 = random.randint(100000, 999999)
                send_mail("Believe in Emerald: ", f"Greetings from Emerald, Your email verification OTP after using forgot password: {ot1}", EMAIL_HOST_USER, [eml1])
                messages.success(request, f"OTP sent to {eml1}")
                return render(request, 'fp2.html')
        otconf = request.POST.get('otp1')
        if ot1 == int(otconf):
            print("Yes")
            return redirect('changep')
        else:
            messages.error(request, "Wrong OTP entered")
        messages.success(request, "Be patient, we are sending you an OTP")
    return render(request, 'fp1.html')   

#Update Password
########################################################################
# @csrf_exempt
def update_password(request):
    global id1
    if request.method == 'POST':
        ps1 = request.POST.get('em1')
        ps2 = request.POST.get('em2')
        if ps1 == ps2:
            entity = get_object_or_404(User_auth, pk=id1)
            entity.password = make_password(ps2)
            entity.save()
            messages.success(request, "You successfully updated your password")
            time.sleep(2)
            return redirect('home')
        else:
            messages.error(request, "Password do not match!")
    return render(request, 'changep.html')