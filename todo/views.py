from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def signup(request):
    if request.method=='POST':
        fnm=request.POST.get("fnm")
        emailid=request.POST.get("email")
        pwd=request.POST.get("pwd")
        print(fnm, emailid, pwd)

       
        if User.objects.filter(username=fnm).exists():
            messages.info(request, 'Account already exists. Please log in.')
            return redirect('/login')


        my_user=User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('/login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm, pwd)

        user=authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todo')
        else:
            return redirect('/signup')
    return render(request, "login.html")


def todo(request):
    if request.method=="POST":
        title=request.POST.get('title')
        print(title)
        obj=models.TODO(title=title, user=request.user)
        obj.save()

        result=models.TODO.objects.filter(user=request.user).order_by('date')
        return redirect('/todo', {'result':result})
    result=models.TODO.objects.filter(user=request.user).order_by('date')
    return render(request, "todo.html", {'result':result})



def edit_todo():
    