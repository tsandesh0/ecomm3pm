# Generated by Django 4.0.4 on 2022-05-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('', 'Default')], max_length=300),
        ),
    ]
