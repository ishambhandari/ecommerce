# Generated by Django 2.2 on 2019-07-09 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190709_1709'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='OrderItems',
        ),
    ]
