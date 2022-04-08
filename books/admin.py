from django.contrib import admin
from .models import Author,Category,Book,MyCart, Orders
# Register your models here.

class bookfilter(admin.ModelAdmin):
    list_display = ('title','printed_year')
class orderfilter(admin.ModelAdmin):
    list_display = ('person','order_id','items','ordered_on')
class cartfilter(admin.ModelAdmin):
    list_display = ('person','book','status','added_on')
    
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book,bookfilter)
admin.site.register(MyCart,cartfilter)
admin.site.register(Orders,orderfilter)

admin.sites.AdminSite.site_header = 'E-bookstore admin '
admin.sites.AdminSite.site_title = 'administration panel'
admin.sites.AdminSite.index_title = 'E-book Admin panel'