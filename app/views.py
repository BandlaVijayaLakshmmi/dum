from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
from app.forms import *
def home(request):
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