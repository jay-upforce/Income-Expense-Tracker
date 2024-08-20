# Generated by Django 5.0.7 on 2024-08-14 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomField_app', '0001_initial'),
        ('transaction_app', '0002_remove_transaction_category_transaction_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='custom_fields',
            field=models.ManyToManyField(related_name='transactions', to='CustomField_app.customfield'),
        ),
    ]
