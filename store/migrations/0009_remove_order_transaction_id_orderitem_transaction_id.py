# Generated by Django 4.1 on 2023-01-30 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_order_product_order_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True, verbose_name='Тапсырыс номері'),
        ),
    ]
