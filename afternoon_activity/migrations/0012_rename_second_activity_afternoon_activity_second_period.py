# Generated by Django 4.2.9 on 2024-05-10 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0011_remove_afternoon_activity_counselor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='afternoon_activity',
            old_name='second_activity',
            new_name='second_period',
        ),
    ]
