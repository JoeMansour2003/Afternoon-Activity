# Generated by Django 4.2.9 on 2024-05-13 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0023_remove_counselor_cabin_counselor_sessioncabin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='sessionCabin',
        ),
        migrations.AddField(
            model_name='counselor',
            name='sessionCabin',
            field=models.ManyToManyField(blank=True, null=True, related_name='counselors_cabin', to='afternoon_activity.sessioncabin'),
        ),
    ]
