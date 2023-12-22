from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .utils import generate_otp, format_email, EmailUser
from django.core.cache import cache
# Create your views here.

def home(request):
    '''Home page view'''
    if request.user.is_authenticated:
        return render(request,'user_authentication/home.html',{'name':request.user})
    else:
        return render(request,'user_authentication/home.html')
    
    
def about(request):
    '''About page view'''
    if request.user.is_authenticated:
        return render(request,'user_authentication/about.html')
    else:
        return render(request,'user_authentication/about.html')
    
    
def rule(request):
    '''Rules page view'''
    if request.user.is_authenticated:
        return render(request,'user_authentication/rule.html')
    else:
        return render(request,'user_authentication/rule.html')
        

def signup(request):
    '''User SignUp view'''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SingUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Your account has been created successfully')
                form.save()
                return redirect('profile')
        else : 
            form = SingUpForm()
        template_path = 'user_authentication/signup.html'
        return render(request, template_path, {'form' : form})
    else:    
        return render(request,'user_authentication/home.html',{'name':request.user_name,'form':form})
    
    
def user_login(request):
    '''User login view'''
    if request.user.is_authenticated:
        return render(request,'user_authentication/profile.html',{'name':request.user}) 
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data = request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pas = form.cleaned_data['password']
            user = authenticate(username=user_name,password = user_pas)
            if user is not None:
                login(request,user)
                # print(request.session.get('ip', None)) # client ip
                # print('success')
                messages.success(request,'Log in successfully')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request,'user_authentication/login.html',{'form':form})
            
            
            
def profile(request):
    '''Profile page view'''
    if request.user.is_authenticated:
        login_count = cache.get('count', version=request.user.pk)
        print("login count :", login_count)
        return render(request,'user_authentication/profile.html',{'name':request.user, 'login_count': login_count}) 
    else:
        return redirect('login')

def user_logout(request):
    '''User logOut page view'''
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')
    
def update_user_details(request):
    '''User update information page'''
    if request.method == 'POST':
        form = ChagneUserData(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Update Successfully')
            return redirect('profile')
    else:
        form = ChagneUserData(instance=request.user)
    return render(request, 'user_authentication/update_data.html', {'form': form})


def change_password(request): 
    '''User password change page view'''
    if not request.user.is_authenticated: 
        return redirect('login')
    if request.method == 'POST': 
        form = CustomSetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid(): 
            form.save()
            messages.warning(request,'Successfully changed your password')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else: 
            form = CustomSetPasswordForm(user=request.user)
        return render(request,'user_authentication/change_pass.html', {'form' : form})
    else:
        form = CustomSetPasswordForm(user=request.user)
        return render(request,'user_authentication/change_pass.html', {'form' : form})


def forgot_password(request):
    '''If user forgot password'''
    if request.method == 'POST':
        # email = request.POST.get('email')
        form = EmailForOTPForm(data= request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Email doesn't match")
                return redirect('login')
            
            otp = generate_otp()  # generate otp
            try: 
                print('email')
                email_body = format_email(user, otp = otp, send_otp = True) #format email body
                EmailUser.send_email(email_body) #send email
            except Exception as e: 
                messages.warning(request, "OTP didn't send, some info maybe missing")
                print(e)
                return redirect('login')
            
            # Store user_id and OTP in session
            request.session['username'] = user.username
            request.session['otp'] = otp
            return redirect('validate_otp')
    form = EmailForOTPForm()
    return render(request, 'user_authentication/send_otp_email.html', {'form': form})


def validateOTP(request):
    '''OTP validation page which sent in email'''
    if request.method == 'POST':
        username = request.session.get('username') # get username from seassion
        stored_otp = request.session.get('otp')

        form = OTPForm(data= request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == stored_otp:
                return redirect('set_new_password')
            messages.warning(request, 'Invalid OTP. Please try again.')
    
    form = OTPForm()
    return render(request, 'user_authentication/otp_form.html', {'form': form})



def set_new_password(request):
    '''Set newpassword view'''
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.warning(request, "User not found!")
        return redirect('login')

    if request.method == 'POST':
        form = NewPasswordForm(data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            request.session.flush() # delete session
            # update_session_auth_hash(request, user)  # Update the user's session to prevent them from being logged out
            messages.success(request, 'Successfully changed your password, now you can login')
            return redirect('login')
    else:
        form = NewPasswordForm()
    return render(request, 'user_authentication/set_new_password.html', {'form': form})