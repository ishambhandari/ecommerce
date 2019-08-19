# Generated by Django 2.2 on 2019-07-09 17:21

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190709_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(default=core.models.get_item, on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='core.OrderItem'),
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
    ]