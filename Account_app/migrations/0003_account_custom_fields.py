# Generated by Django 5.0.7 on 2024-08-13 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0002_alter_account_wallet'),
        ('CustomField_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='custom_fields',
            field=models.ManyToManyField(related_name='accounts', to='CustomField_app.customfield'),
        ),
    ]
