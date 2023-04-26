from django import forms
from django.contrib.auth.models import User


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistartionForm(forms.ModelForm):
     
     password = forms.CharField(label='password',widget=forms.PasswordInput)   
     password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)   
     class Meta:
          model = User
          fields = {'username','email','first_name'}

     def check_password(self):
          if self.cleaned_data['password'] != self.clenned_data['password2']:
             raise forms.ValidationError('passwords do not match')
          return self.cleaned_data['password2']