from django import forms
from models import Profile, tonight
from django.contrib.admin import widgets

from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#from tools import calculate_age

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput())
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput())
    email=forms.EmailField(required=False)
    birth_date = forms.DateField()
    avatar = forms.ImageField()
    gender = forms.CharField(max_length=1)
    status = forms.CharField(max_length=1)
    religion = forms.BooleanField(label='Shomer Shabbat')
    children =forms.BooleanField(label='Yes/No')
    descrption = forms.CharField(label='Title Description',widget=forms.Textarea)
    #age = calculate_age(birth_date)

class ProfileF(forms.ModelForm):
    class Meta:
        model = Profile
        fields =('__all__')
        #fields = ('email','birth_date' ,'avatar','gender','status','religion','children','descrption')

#class UserForm(UserCreationForm):
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #fields =('__all__')
        fields = ('country', 'city', 'birth_date', 'avatar', 'gender', 'status', 'religion', 'children', 'descrption')

class ToNightForm(forms.ModelForm):
    class Meta:
        model = tonight
        #fields =('__all__')
        fields = ('Title', 'flyer', 'comment', 'telephone', 'city', 'country', 'event_date')

class SearchProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('search_country', 'search_city', 'search_gender', 'search_status', 'search_religion', 'search_children')
