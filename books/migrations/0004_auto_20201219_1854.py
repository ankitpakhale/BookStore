# Generated by Django 3.1.2 on 2020-12-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20201218_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='cat_name',
        ),
        migrations.AlterField(
            model_name='mycart',
            name='added_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
