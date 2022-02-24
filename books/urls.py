from django.urls import path
from .views import shoplist, book_view, add_to_cart, remove_cart, search, my_filter, place_order, myaccount, qrshow, book_preview,speak,about,contact,invoice

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
    path('qr/<int:order_id>', qrshow, name='qr'),
    path('preview/<int:pk>', book_preview, name='preview'),
    path('speak/<int:pk>',speak,name='speak'),
    path('invoice/<int:pk>',invoice,name='invoice'),
]

# old