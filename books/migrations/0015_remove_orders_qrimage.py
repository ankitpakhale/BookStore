# Generated by Django 4.0.2 on 2022-03-03 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_mycart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='qrimage',
        ),
    ]
