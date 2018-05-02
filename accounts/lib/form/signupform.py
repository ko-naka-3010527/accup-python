from django import forms

class SignupForm(forms.Form):
    userid = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100)
    password_confirm = forms.CharField(max_length=100)
    email = forms.EmailField()

class UpdateForm(forms.Form):
    updatepwd = forms.IntegerField(max_value=1,min_value=0)
    password = forms.CharField(max_length=100,required=False)
    password_confirm = forms.CharField(max_length=100,required=False)
    email = forms.EmailField(required=False)
    current_password = forms.CharField(max_length=100)
   
