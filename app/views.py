from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
from app.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def registration(request):
    ufd=userform()
    pfd=profileform()
    d={'ufd':ufd,'pfd':pfd}
    if request.method=='POST' and request.FILES:
        ufd=userform(request.POST)
        pfd=profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            nsuo=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            nsuo.set_password(password)
            nsuo.save()
            nspo=pfd.save(commit=False)
            nspo.username=nsuo
            nspo.save()
            send_mail('Registration',
                      "Succefully Registration is Done",
                      'bandlavijayalakshmi0904@gmail.com',
                      [nsuo.email],
                      fail_silently=False
                      )
            return HttpResponse('registration is successfully')
        else:
            return HttpResponse('invalid-data')
    
    return render(request,'registration.html',d)
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    