# Generated by Django 4.0.4 on 2022-06-08 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
    ]
