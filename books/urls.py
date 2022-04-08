from django.urls import path
from .views import shoplist, book_view, add_to_cart, remove_cart,invoice,search, my_filter, place_order, myaccount, book_preview,about,contact,allInvoices,perticularInvoices

urlpatterns = [
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('shop/', shoplist, name='shop'),
    path('bookview/<int:pk>/', book_view, name='book_view'),
    path('cart/', add_to_cart, name='cart'),
    path('deleteitem/<int:id>/', remove_cart, name='delete'),
    path('search/', search, name='search'),
    path('filter/', my_filter, name='my_filter'),
    path('placeorder/', place_order, name='place_order'),
    path('myaccount/', myaccount, name='myaccount'),
    
    path('allInvoices/', allInvoices, name='allInvoices'),
    path('perticularInvoices/<int:pk>', perticularInvoices, name='perticularInvoices'),
    
    path('preview/<int:pk>', book_preview, name='preview'),
    path('invoice/<int:pk>',invoice,name='invoice'),

]


# new