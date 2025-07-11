# Generated by Django 5.1.7 on 2025-04-22 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SenderID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sender_id', to='web.usersession')),
            ],
        ),
    ]
