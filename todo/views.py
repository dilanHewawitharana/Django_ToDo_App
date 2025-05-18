from django . shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST['fnm']
        emailid = request.POST['emailid']
        pwd = request.POST['pwd']
        print(fnm, emailid, pwd)

        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/loginn')

    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST['fnm']
        pwd = request.POST['pwd']
        print(fnm, pwd)

        user = authenticate(username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todopage')
        else:
            return redirect('/loginn')
    return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def todo(request):
    if request.user.is_anonymous:
        return redirect('/loginn')
    if request.method == 'POST':
        title = request.POST['title']
        print(title)
        ins = TODOO(title=title, user=request.user)
        ins.save()

        res = models.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

@login_required(login_url='/loginn')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST['title']
        print(title)
        obj = TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')
    
    obj = models.TODOO.objects.get(srno=srno)
    print(obj.title)
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/loginn')
def delete_todo(request, srno):
    obj = TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/loginn')