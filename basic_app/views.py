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

        if password1 == password2:
            if Person.objects.filter(email=email).exists():
                q = messages.info(request, 'email address already exist')
                print(q)

                return redirect('basic_app:register')

            else:
                data = Person.objects.create(
                    first_name=first_name, last_name=last_name, email=email, password=password1)
                data.save()
                print('done')
                return redirect('basic_app:index')
                messages.success(request, 'Your account successfully created')
               
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


def forgot(request):
    if request.POST:
        data = request.POST['email']
        print(data)
        
        valid = Person.objects.get(email=data)
        print(valid)

        otp = ''
        rand = random.choice('0123456789')
        rand1 = random.choice('0123456789')
        rand2 = random.choice('0123456789')
        rand3 = random.choice('0123456789')
        otp = rand + rand1 + rand2 + rand3
        print(f"Your OTP is {otp}")
        

        request.session['otp'] = otp
        return redirect('basic_app:OTPCHECK')
        # try:
        #     valid = Person.objects.get(email=data)
        #     print(valid)

        #     otp = ''
        #     rand = random.choice('0123456789')
        #     rand1 = random.choice('0123456789')
        #     rand2 = random.choice('0123456789')
        #     rand3 = random.choice('0123456789')
        #     otp = rand + rand1 + rand2 + rand3
        #     print(f"Your OTP is {otp}")
            
        #     msg = EmailMessage()
        #     msg.set_content(f'''     
        #     Thank you for contacting with us.
        #     Your OTP is {otp}
        #     ''')
            
        #     msg['Subject'] = 'Online Book Store'
        #     msg['From'] = 'akp3067@gmail.com'
        #     msg['To'] = 'ankitpakhale786@gmail.com'
        #     msg['To'] = '{valid}'
            
        #     # to get OTP in Email
        #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #     print("working1")
        #     server.login("akp3067@gmail.com", "password")
        #     print("working2")
        #     server.send_message(msg)
        #     print("working3")
        #     server.quit()

        #     request.session['otp'] = otp

        #     return redirect('OTPCHECK')

        # except:
        #     return HttpResponse('<a href=""> You Have Entered Wrong Email Id... </a>')
        
        
    return render(request,'basic_app/forgot.html')

def otpCheck(request):
    if 'otp' in request.session.keys():
        if request.POST:
            otp1 = request.POST['otpuser']
            print("OTP1 is "+otp1)
            otp = request.session['otp']
            print("OTP is "+otp)
            if otp1 == otp:
                # del request.session['otp']
                print("You Are Ready to Create New Password...")

                # user = Person.objects.get(email = otp1)
                # request.session['email'] = user.email
                

                return redirect('basic_app:NEWPASS')
            else:
                del request.session['otp']
                return redirect('basic_app:FORGOT')
        return render(request,'basic_app/otpCheck.html')
    else:
        return redirect('basic_app:login')

def newPassword(request):
    print("Inside New Pass FUNCTION")
    # if 'otp' in request.session.keys():
    if 'otp' in request.session:
        print("Inside New Pass if CONDITION")
        if request.POST:
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            print(pass1+" : "+pass2)
            if pass1 == pass2:
                print("Both password is correct")

                # obj = signUp.objects.get(email =  request.POST.get('email'))

                obj = Person.objects.get(email = request.session['email'])

                obj.password = pass1
                obj.confirmPassword = pass2
                obj.save()
                del request.session['otp']
                # return redirect('HOME')
                return redirect('basic_app:login')
            else:
                return HttpResponse("<h1>Password must be same</h1>")
        return render(request,'basic_app/newPass.html')
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

            data.first_name = request.POST.get('firstname') or None
            data.last_name = request.POST.get('lastname') or None
            data.email = request.POST.get('email') or None
            data.password = request.POST.get('passoword') or None
            data.save()
            print("Details successfully updated")
            return redirect('basic_app:logout')