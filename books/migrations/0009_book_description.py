# Generated by Django 3.1.2 on 2020-12-29 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_book_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
    ]