# Generated by Django 2.2 on 2019-08-27 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_addres',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BillingAddress'),
        ),
    ]
