from django.shortcuts import render, redirect
from .models import Person
from django.http import HttpResponse
from books.models import Category,Book,Author
from django.contrib import messages
import qrcode

import random
import smtplib
from email.message import EmailMessage

# Create your views here.


def index(request):
    if request.session.has_key('email'):
        cat=Author.objects.all()
        user1 = request.session['email']
        print(user1)
        per = Person.objects.get(email=user1)
        print(per)
        print(per.first_name)
        log = 'Logout'
        return render(request, 'basic_app/index.html', {'per': per, 'log': log,"cat":cat})
    return render(request, 'basic_app/index.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        forgot_ans = request.POST.get('forgot_ans')

        if password1 == password2:
            if Person.objects.filter(email=email).exists():
                q = messages.info(request, 'email address already exist')
                print(q)

                return redirect('basic_app:register')

            else:
                data = Person.objects.create(first_name=first_name, last_name=last_name, email=email, password=password1, forgot_ans = forgot_ans)
                data.save()
                print('done')
                messages.success(request, 'Your account successfully created')
                return redirect('basic_app:index')
        else:
            messages.info(request, 'Password does not match')
            return redirect('basic_app:register')
    return render(request, 'basic_app/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        m = Person.objects.get(email=email)
        if m.password == password:
            request.session['email'] = email
            messages.info(request, f'you are now logged in{email}')
            return redirect('basic_app:index')
        else:
            messages.warning(request, 'Please input correct password')
            return redirect('basic_app:login')
    else:
        return render(request, 'basic_app/login.html')

def Confirm(request):
    if request.POST:
        data = request.POST['conf']
        try:
            valid = Person.objects.get(forgot_ans=data)
            if valid:
                print("Valid ans")
                request.session['user'] = valid.email
                print("redirecting to forgot")
                return redirect('basic_app:FORGOT')
            else:
                print("INValid ans")
                return HttpResponse('Wrong Answer')    
        except:
            return HttpResponse('Wrong Answer')
    return render(request,'basic_app/Confirm.html')

def forgot(request):
    print("inside  1")
    if 'user' in request.session:
        print("inside 2")
        if request.POST:
            print("inside 3")
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            
            if pass1 == pass2:
                obj = Person.objects.get(email=request.session['user'])
                obj.password = pass2
                obj.save()
                del request.session['user']
                return redirect('basic_app:login')
            else:
                messages.add_message(request, messages.ERROR, 'Not Same')
        return render(request,'basic_app/forgot.html')
    return redirect('basic_app:login')

def authorwise(request,name):
    if request.session.has_key('email'):
        auth=Author.objects.get(name=name)
        book=Book.objects.all().filter(authors=auth).distinct()
        return render(request,'basic_app/authwise.html',{'cat':auth,'book':book})
    else:
        auth=Author.objects.get(name=name)
        book=Book.objects.all().filter(authors=auth).distinct()
        return render(request,'basic_app/authwise.html',{'cat':auth,'book':book})


def catwisebook(request,cat_name):
    if request.session.has_key('email'):
        cat=Category.objects.get(cat_name=cat_name)
        book=Book.objects.all().filter(categories=cat).distinct()
        return render(request,'basic_app/catwise.html',{'cat':cat,'book':book})
    else:
        cat=Category.objects.get(cat_name=cat_name)
        book=Book.objects.all().filter(categories=cat).distinct()
        return render(request,'basic_app/catwise.html',{'cat':cat,'book':book})


def logout(request):
    if request.session.has_key('email'):
        del request.session['email']
        messages.info(request, 'you are logged out Now')
        return redirect('basic_app:index')


def profile_edit(request):
    if request.session.has_key('email'):
        data = Person.objects.get(email=request.session['email'])
        if request.method == 'POST':

            if request.POST.get('firstname') == '':
                pass
            else:
                data.first_name = request.POST.get('firstname')
                
            if request.POST.get('lastname') == '':
                pass
            else:
                data.last_name = request.POST.get('lastname')
                
            if request.POST.get('email') == '':
                pass
            else:
                data.email = request.POST.get('email')
          
            data.save()
            
            print("Details successfully updated")
            return redirect('basic_app:logout')