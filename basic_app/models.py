from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    password = models.CharField(max_length=80)
    #myorder = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name