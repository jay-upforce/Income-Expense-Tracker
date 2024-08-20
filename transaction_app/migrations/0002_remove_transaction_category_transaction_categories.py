# Generated by Django 5.0.7 on 2024-08-12 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category_app', '0001_initial'),
        ('transaction_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.AddField(
            model_name='transaction',
            name='categories',
            field=models.ManyToManyField(related_name='transactions', through='transaction_app.TransactionCategory', to='Category_app.category'),
        ),
    ]
