# Generated by Django 3.1.2 on 2020-12-29 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='audio',
            field=models.FileField(null=True, upload_to='audiofile'),
        ),
    ]