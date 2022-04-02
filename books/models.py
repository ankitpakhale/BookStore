from django.db import models
import datetime
from basic_app.models import Person
from django.utils.timezone import utc
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Category(models.Model):
    cat_name = models.CharField(max_length=80)

    def __str__(self):
        return self.cat_name


class Book(models.Model):
    title = models.CharField(max_length=80)
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    cover = models.ImageField(upload_to='covers')
    price = models.PositiveIntegerField()
    printed_year = models.PositiveSmallIntegerField()
    preview = models.FileField(upload_to='bookpdf',null=True)
    description = models.TextField(null=True)

    #fullbook = models.FileField(upload_to='fullbook',null=True)

    def __str__(self):
        authors = ', '.join([str(author) for author in self.authors.all()])
        return ', '.join((
            self.title,
            authors,
            str(self.printed_year)
        ))

class MyCart(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    quantity=models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on= models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.person.first_name
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    items = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=80)
    ordered_on = models.DateTimeField(auto_now_add=True,null=True)
    qrimage = models.ImageField(upload_to='qrimage',blank=True,null=True)
    invoice = models.FileField(default='')

    def __str__(self):
        return self.items