# Generated by Django 5.0.3 on 2024-03-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0005_counselor_email_counselor_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counselor',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
