# Generated by Django 3.1.2 on 2020-12-28 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_orders_qrimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='preview',
            field=models.FileField(null=True, upload_to='bookpdf'),
        ),
    ]
