# Generated by Django 5.1.4 on 2024-12-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Сумма оплаты'),
        ),
    ]
