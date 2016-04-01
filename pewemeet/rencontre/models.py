from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from registration.signals import user_registered
from cities_light.models import City, Country
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    city = models.ForeignKey(City)
    search_city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    birth_date = models.DateField(blank=False)
    avatar = models.ImageField(null=True, blank=True, upload_to="static/avatars/")
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    STATUS_CHOICES = (
        ('D', 'Divorced'),
        ('S', 'Single'),
        ('O', 'Others'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    religion = models.BooleanField('Shomer Shabbat', default=True)
    children = models.BooleanField('Children', default=False)
    descrption = models.TextField('Title Description', default='', blank=True)
    search_city = models.ForeignKey(City, related_name='search_city')
    search_country = models.ForeignKey(Country, related_name='search_country',default='IL')
    search_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    search_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    search_religion = models.BooleanField(default=False)
    search_children = models.BooleanField(default=False)
    #homepage = models.URLField()

    def __str__(self):
        return self.user.username

def assure_user_profile_exists(pk):
        """
        Creates a user profile if a User exists, but the
        profile does not exist.  Use this in views or other
        places where you don't have the user object but have the pk.
        """
        user = User.objects.get(pk=pk)
        try:
            # fails if it doesn't exist
            user = user.userprofile
        except Profile.DoesNotExist, e:
            userprofile = Profile(user=user)
            userprofile.save()
        return

def create_user_profile(**kwargs):
        Profile.objects.get_or_create(user=kwargs['user'])

user_registered.connect(create_user_profile)

class tonight(models.Model):
    Title = models.CharField(max_length=50)
    flyer = models.ImageField(null=True, blank=True, upload_to="static/fliyers/")
    comment = models.TextField(default='', blank=True)
    telephone = PhoneNumberField()
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    event_date = models.DateField('Date Event', blank=False, default='')

    def __str__(self):
        return self.Title

