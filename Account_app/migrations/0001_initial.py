# Generated by Django 5.0.7 on 2024-08-09 06:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Wallet_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('acc_num', models.CharField(max_length=255)),
                ('gst_no', models.CharField(max_length=20)),
                ('pan_no', models.CharField(max_length=255)),
                ('bank_Details', models.TextField()),
                ('address', models.TextField()),
                ('phone_no', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('notes', models.TextField()),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='Wallet_app.wallet', verbose_name='accounts have multiple wallets')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
