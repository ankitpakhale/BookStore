# Generated by Django 3.1.2 on 2020-12-25 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0001_initial'),
        ('books', '0004_auto_20201219_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_amount', models.CharField(max_length=80)),
                ('ordered_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.person')),
            ],
        ),
    ]
