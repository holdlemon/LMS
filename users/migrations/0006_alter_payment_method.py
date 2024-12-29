# Generated by Django 5.1.4 on 2024-12-26 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('cash', 'Наличные'), ('transfer', 'Перевод')], default='cash', max_length=50, verbose_name='Способ оплаты'),
        ),
    ]
