from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    password = models.CharField(max_length=80)
    forgot_ans = models.CharField('Write Something Which Help You To Change Your Password',max_length=100,default='')
    #myorder = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name