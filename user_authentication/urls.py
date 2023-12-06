from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.home,name='home'),
   path('about/',views.about,name='about'),
   path('rule/',views.rule,name='rule'),
   path('signup/',views.signup,name='signup'),
   path('profile/',views.profile,name='profile'),
   path('login/',views.user_login,name='login'),
   path('logout/',views.user_logout,name='logout'),
   path('update/',views.update_user_details,name='update'),
   path('change_pass/',views.change_password,name='change-pass'),
   path('send-otp-email/',views.forgot_password,name='send-otp-email'),
   path('reset-password-OTP-validation/',views.validateOTP,name='validate_otp'),
   path('set-newpassword/',views.set_new_password,name='set_new_password'),
   
]