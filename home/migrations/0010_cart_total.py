# Generated by Django 4.0.4 on 2022-06-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_cart_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=1),
        ),
    ]
