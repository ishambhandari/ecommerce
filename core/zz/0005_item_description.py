# Generated by Django 2.2 on 2019-07-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is the test description. sssasbd  nasndndnan sjakdnfjklsgnajldfkgn '),
            preserve_default=False,
        ),
    ]
