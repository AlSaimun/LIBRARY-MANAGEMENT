from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import MinLengthValidator

class SingUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}),help_text="enter first name")
    last_name = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class ChagneUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
        
    def clean(self):
        email = self.cleaned_data['email']
        user = self.instance
        if User.objects.filter(email=email).exclude(pk= user.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
    
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Confirm Password'    

class EmailForOTPForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'required'}))

class OTPForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))


class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'required'}),
        validators=[MinLengthValidator(limit_value=8, message="Password must be at least 8 characters.")]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'required'}))

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        print(new_password, confirm_password)
        if new_password and confirm_password and new_password != confirm_password: # check new password and confirm password same
            raise forms.ValidationError("new password and confirm password are not same!")