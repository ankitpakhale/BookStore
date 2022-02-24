from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Book, Author, Category, MyCart, Orders
from basic_app.models import Person
from django.contrib import messages
from django.db.models import Q
from .forms import FilterSearchForm
import smtplib
from email.message import EmailMessage
import qrcode
from bookstore.settings import BASE_DIR
import os
import random
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import date,datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def about(request):
    return render(request,'books/about.html')



def contact(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mymsg = request.POST['msg']
        print(mymsg)

        msg = EmailMessage()
        msg.set_content(f'''
        Thank you for connecting with us.

        Full name: {firstname}
        Full name: {lastname}
        Email: {email}
        Msg: {mymsg}
        ''')

        msg['Subject'] = 'Cronicle Bookstore'
        msg['From'] = "hkp6565@gmail.com"
        msg['To'] = "hardikvekariya911@gmail.com"

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("hkp6565@gmail.com", "shivam@789")
        server.send_message(msg)
        server.quit()
        messages.info(request,'Message had been sent. Thank you for your notes.')
        return redirect('books:contact')
    return render(request,'books/contact.html')

def shoplist(request):
    a=Author.objects.all()
    b = Book.objects.all()
    c=Category.objects.all()
    if request.session.has_key('email'):
        b = Book.objects.all()
        user1 = request.session['email']
        print(user1)
        per = Person.objects.get(email=user1)
        print(per)
        print(per.first_name)
        log = 'Logout'

        return render(request, 'books/shop.html', {'b': b, 'per': per,'c':c,'a':a})

    return render(request, 'books/shop.html', {'b': b,'c':c,'a':a})


def book_view(request, pk):

    p = get_object_or_404(Book, pk=pk)
    if request.session.has_key('email'):
        p = get_object_or_404(Book, pk=pk)
        user1 = request.session['email']
        # print(user1)
        per = Person.objects.get(email=user1)
       # print(per)
        # print(per.first_name)
        log = 'Logout'
        return render(request, 'books/single_product.html', {'p': p, 'per': per})

    return render(request, 'books/single_product.html', {'p': p})

def book_preview(request, pk):
    c = get_object_or_404(Book,pk=pk)
    response = HttpResponse(c.preview.read(),content_type='application/pdf')
    return response

# def book_read(request,pk):
#     x = get_object_or_404(Book,pk)
#     response = HttpResponse(x.fullbook.read(),content_type='application/pdf')
#     return response

def add_to_cart(request):
    print("inside add_to_cart")
    if request.session.has_key('email'):
        print("Inside first if")
        per = Person.objects.get(email=request.session['email'])
        item = MyCart.objects.filter(person__id=per.id, status=False)
        num = MyCart.objects.filter(person__id=per.id, status=False).count()
        
        total = 0
        for q in item:
            total += q.book.price * q.quantity
            print(q.quantity)
        print(total)
        #log = 'Logout'
        # print(num)
        # print(per.id)
        
        if request.method == 'POST':
            print("Inside second if")
            bid = request.POST['bid']
            print(bid)
            p = Book.objects.get(id=bid)
            if MyCart.objects.filter(book__id=bid, person__id=per.id, status=False).exists():
                print("lululu")
                messages.warning(request, 'Item already in the cart')
                return render(request, 'books/single_product.html', {'p': p, 'per': per})
            else:
                print("inside else condition")
                bk = get_object_or_404(Book, id=bid)
                # per = get_object_or_404(Person,id=per.id)
                # print(per)
                c = MyCart.objects.create(person=per, book=bk)
                try:
                    a=request.POST['qty']
                    print(a)
                    c.quantity = a
                except:
                    c.quantity = 1
                c.save()
                request.session['order_id']=c.id
                messages.warning(request, 'Item has been added to cart')
                return render(request, 'books/single_product.html', {'p': p, 'per': per})
        else:
            print("main else")
            return render(request, 'books/checkout.html', {'item': item, 'num': num, 'per': per, 'total': total})
    else:
        print("main else part 2")
        messages.info(request, 'please login first to access the cart ')
        return redirect('basic_app:login')

def remove_cart(request, id):
    if request.session.has_key('email'):
        y = get_object_or_404(MyCart, id=id)
        y.delete()
        return redirect('books:cart')


def search(request):
    query = request.GET.get('search')
    print(query)
    qset = query.split(' ')
    for q in qset:

        b = Book.objects.filter(Q(title__icontains=q) | Q(
            authors__name__icontains=q) | Q(categories__cat_name__icontains=q)).distinct()
    # except:
    #     b = Book.objects.filter(categories__cat_name__icontains=query)
    # print(query)
    # b = Book.objects.filter(authors__name__icontains=query)
    # print(b)

    # if Book.objects.filter(title__icontains=query) is not None:
    #     b = Book.objects.filter(title__icontains=query)
    #     return render(request,'books/shop.html',{'b':b})
    # else:

    return render(request, 'books/shop.html', {'b': b})


def my_filter(request):
    b = Book.objects.all()
    #c = Category.objects.all()
    category_f = request.GET.get('query')
    arrival = request.GET.get('arrival')
    price_range = request.GET.get('bprice')
    print(price_range)
    #query = request.GET.get('finance')
    # print(query)

    if category_f:
        b = Book.objects.filter(
            Q(categories__cat_name__icontains=category_f)).distinct()
        print(b)
    elif arrival == 'newest':
        b = Book.objects.all().order_by('-printed_year')
        print(b)
    elif arrival == 'oldest':
        b = Book.objects.all().order_by('printed_year')
    elif price_range == 'LTH':
        b = Book.objects.all().order_by('price')
    elif price_range == 'HTL':
        b = Book.objects.all().order_by('-price')
    elif price_range == '00-500':
        b = Book.objects.filter(price__range = (0,500)).order_by('price')
    elif price_range == '500-1000':
        b = Book.objects.filter(price__range = (500,1000)).order_by('price')

    return render(request, 'books/shop.html', {'b': b})


def place_order(request):
    if request.session.has_key('email'):
        per = Person.objects.get(email=request.session['email'])
        item = MyCart.objects.filter(person__id=per.id, status=False)
        total = 0
        books_incart = ''
        for q in item:
            total += q.book.price
            books_incart = q.book.title +','+ books_incart
            #print(total)
            #print(books_incart)
        request.session['Total']=total

        if request.method == 'POST':
            full_name = request.POST['name']
            email = request.POST['email']
            landmark = request.POST['landmark']
            city = request.POST['city']

            # Malking Qrcode
            qrdata = f"""
            name = {full_name}
            email = {email}
            city = {city}
            landmark = {landmark}
            items name = {books_incart}
            amount = {total}
            """ 
            num = random.randint(1111,9999)
            obj = Orders(person=per)
            qr=qrcode.QRCode(version=1,box_size=10,border=5)
            qr.add_data(qrdata)
            qr.make(fit=True)
            img=qr.make_image(fill="black",back_color="white")
            img.save(os.path.join(BASE_DIR,"media/"+ str(num) +".jpeg"))
            y = f'{num}.jpeg'
            my_order = Orders.objects.create(person=per,items=books_incart,order_amount=total,qrimage=y)
            my_order.save()
            print("QR Saved")
            #print(my_order.order_id)

            # ----------- remove item from cart after placed the order ---------- #
            for i in item:
                cart_obj = MyCart.objects.get(id=i.id)
                cart_obj.status = True
                cart_obj.save()

            # ----------- Sending Email to customer -----------
            msg = EmailMessage()
            msg.set_content(f'''
            Thank you for your order.
            order details:

            Full name: {full_name}
            Email: {email}
            city: {city}
            Order Amount: {total}
            Order Id: {my_order.order_id}
            Items name: {books_incart}
            ''')

            msg['Subject'] = 'Cronicle Bookstore'
            msg['From'] = "hkp6565@gmail.com"
            msg['To'] = f"{email}"

            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            print("1st")
            server.login("hkp6565@gmail.com", "shivam@789")
            print("2nd")
            server.send_message(msg)
            print("3rd")
            server.quit()
            print("Successfully mail sent")
            return redirect('books:shop')

    else:
        messages.info(request, 'please login first to access the cart ')
        return redirect('basic_app:login')

def myaccount(request):
    if request.session.has_key('email'):
        data = Person.objects.get(email=request.session['email'])
        my_order = Orders.objects.filter(person__id=data.id)
        
        return render(request, 'books/dashbord.html', {'data': data,'my_order':my_order})
    else:
        return redirect('basic_app:login')

def qrshow(request,order_id):
    q = get_object_or_404(Orders,order_id=order_id)
    return render(request,'books/qr.html',{'q':q})

def speak(request,pk):
    p = get_object_or_404(Book,pk=pk)
    tts = gTTS(text=p.description,lang="en")
    
    filename = os.path.join(BASE_DIR,"media/"+ str(p.id) +".mp3")
    try:    
        tts.save(filename)
        #p.audio = filename
        #p.save()
        playsound.playsound(filename)
    except:
        playsound.playsound(filename)
    if request.session.has_key('email'):
        per = Person.objects.get(email=request.session['email'])
        return render(request,'books/single_product.html',{'p':p,'per':per})
    else:
        return render(request,'books/single_product.html',{'p':p})


def invoice(request,pk):
    x = get_object_or_404(Orders,pk=pk)
    f= open(f'media/invoice/{x.order_id}.txt','w')
    f.write('orderId:'+str(x.order_id))
    f.close()
    print('file done')
    f = f"invoice/{x.order_id}.txt"
    x.invoice = f
    x.save()
    return render(request,'books/invoice.html',{'x':x})


    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    # c = canvas.Canvas(response,pagesize=(200,250),bottomup=0)

