from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from rencontre.forms import UserForm, UserProfileForm, SearchProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response

#from models import Profile
from django import forms
from forms import ProfileForm, ProfileF, ToNightForm
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib.auth.models import User
from rencontre.models import Profile, assure_user_profile_exists, tonight
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F

# Use the login_required() decorator to ensure only those logged in can access the view.

class UserProfileDetail(DetailView):
    model = Profile
    context_object_name = "Profile"
    fields = '__all__'

class UserProfileUpdate(UpdateView):
    model = Profile
    #fields = '__all__'
    fields = ('birth_date' ,'avatar','gender','status','religion','children','descrption')
    #fields = ('birth_date','gender','status','religion','descrption',)
    #fields = ('homepage',)

    def get(self, request, *args, **kwargs):
        assure_user_profile_exists(kwargs['pk'])
        return (super(UserProfileUpdate, self).
                get(self, request, *args, **kwargs))


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'rencontre/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                #userlogged = request.user.id
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rencontre/login.html', {})

#@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login')

def message(request):
    return render(request, 'rencontre/message.html', {})

class ListeProfile(ListView):
    model = Profile
    context_object_name = "All_profiles"
    template_name = "rencontre/Profile_list.html"
    queryset = Profile.objects.filter(gender=F("search_gender"))
    #queryset = Profile.objects.filter(gender="F")
    #paginate_by = 100

class SearchProfile(UpdateView):
    model = Profile
    #context_object_name = "All_profiles"
    template_name = "rencontre/SearchProfile.html"
    form_class = SearchProfileForm
    #queryset = Profile.objects.filter(gender__exact=F('search_gender'))
    #paginate_by = 100
    success_url = "/"
    template_name_suffix = '_update_form'

class LireProfile(DetailView):
    model = Profile
    context_object_name = "Profile"
    template_name = "rencontre/Profile_detail.html"


class CreateProfile(CreateView):
    model = Profile
    template_name = 'rencontre/Profile_new.html'
    form_class = ProfileF
    success_url = reverse_lazy(ListeProfile)

class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'rencontre/Profile_update.html'
    form_class = ProfileF
    #success_url = reverse_lazy(UserProfileDetail)
    success_url = "/"
    template_name_suffix = '_update_form'

class ListeToNight(ListView):
    model = tonight
    context_object_name = "All_ToNight"
    template_name = "rencontre/tonight_list.html"
    #paginate_by = 100

class DetailToNight(DetailView):
    model = tonight
    context_object_name = "tonight"
    template_name = "rencontre/tonight_detail.html"

