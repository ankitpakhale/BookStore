from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Book, Author, Category, MyCart, Orders
from basic_app.models import Person
from django.contrib import messages
from django.db.models import Q
from .forms import FilterSearchForm
import smtplib
from email.message import EmailMessage
from bookstore.settings import BASE_DIR
import os
import random
import time
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import date,datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import get_template
from xhtml2pdf import pisa

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

        msg['Subject'] = 'E- Bookstore'
        msg['From'] = "mailtesting681@gmail.com"
        msg['To'] = email

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("mailtesting681@gmail.com", "mailtest123@'")
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
        
        # request.session['tot'] = total
        
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

# ---------------------------------------------------------------------------------------

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
# ---------------------------------------------------------------------------------------

def place_order(request):
    if request.session.has_key('email'):
        per = Person.objects.get(email=request.session['email'])
        item = MyCart.objects.filter(person__id=per.id, status=False)
        
        itemQty = MyCart.objects.filter(person=per)
        print(itemQty[0].quantity,"This is a new qty")
        
        # total = request.session['tot']
        # print(total,"sjiascibak") 
        # del request.session['tot']
        
        total1 = 0
        books_incart = ''
        for q in item:
            total1 += q.book.price
            books_incart = q.book.title +','+ books_incart
            #print(total1)
            #print(books_incart)
        # print(per,books_incart,total1,"---------------00000000000000")

        if request.method == 'POST':
            full_name = request.POST['name']
            email = request.POST['email']
            landmark = request.POST['landmark']
            city = request.POST['city']

            num = random.randint(1111,9999)
            obj = Orders(person=per)
            my_order = Orders.objects.create(person=per,items=books_incart,order_amount=total1)
            my_order.save()
            

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
            Order Amount: {total1}
            Items name: {books_incart}
            
            Your Order will be delivered within next 5 days
            ''')

            msg['Subject'] = 'E-Bookstore'
            msg['From'] = "mailtesting681@gmail.com"
            msg['To'] = f"{email}"

            # Send the message via our own SMTP server.
            print("0")
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            print("1")
            server.login("mailtesting681@gmail.com", "mailtest123@")
            print("2")
            server.send_message(msg)
            print("3")
            server.quit()
            print("4")

            # print(f"Full name: {full_name}, Email: {email}, city: {city}, Order Amount: {total1}, Items name: {books_incart}")
            
            # print(f"{full_name}, {email}, {city}, {total1}, {books_incart},55555555555555555555")
            print("Successfully mail sent")
            
            print("redirecting to html to pdf")
          
            data = {'FullName':full_name,
                    'Email':email,
                    'city':city,
                    'OrderAmount':total1, 
                    'books_incart':books_incart, 
                    'per':per}
            pdf = render_to_pdf('books/GeneratePdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
            
            # return redirect('books:shop')
    else:
        messages.info(request, 'please login first to access the cart ')
        return redirect('basic_app:login')
    return render(request,'books/checkout.html')

def myaccount(request):
    if request.session.has_key('email'):
        data = Person.objects.get(email=request.session['email'])
        my_order = Orders.objects.filter(person__id=data.id)
        
        return render(request, 'books/dashbord.html', {'data': data,'my_order':my_order})
    else:
        return redirect('basic_app:login')
    
def allInvoices(request):
    if request.session.has_key('email'):
        data = Person.objects.get(email=request.session['email'])
        my_order = Orders.objects.filter(person__id=data.id)
        return render(request, 'books/allInvoices.html', {'data': data,'my_order':my_order})
    else:
        return redirect('basic_app:login')
    
def perticularInvoices(request,pk):
    if request.session.has_key('email'):
        
        data = Person.objects.get(email=request.session['email'])
        my_order = Orders.objects.filter(person__id=data.id)
        
        # x = get_object_or_404(Orders,pk=pk)
        # f= open(f'media/invoice/{x.order_id}.txt','w')
        # f.write('orderId:'+str(x.order_id))
        # f.close()
        # print('file done')
        # # f = f"invoice/{x.order_id}.txt"
        # # x.invoice = f
        # x.save()

        data = {
            # 'x':x
            'data': data,
            'my_order':my_order
        }
        
        pdf = render_to_pdf('books/GeneratePdf1.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        
    else:
        return redirect('basic_app:login')

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