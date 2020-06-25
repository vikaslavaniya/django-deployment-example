from django.shortcuts import render
from app.forms import UserProfileInfoForm,UserForm
from django.contrib.auth.models import User
from app.models import UserProfileInfo


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect ,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required






# Create your views here.
def index(request):
    return render(request,'app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required
def special(request):
    return HttpResponse("You are logged in")

def register(request):
    registered = False

    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():
            user =user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            # if 'profile_pic' in request.Files:
            #     profile.profile_pic=request.Files['profile_pic']


            profile.save()

            registered=True
        else:
            print("profile pic error")

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()


    return render(request,'app/registration.html',
    {'user_form':user_form,'profile_form':profile_form,'registered':registered})




def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("not activated")


        else:
            return HttpResponse("login failed")
    else:
        return render(request,'app/login.html')
