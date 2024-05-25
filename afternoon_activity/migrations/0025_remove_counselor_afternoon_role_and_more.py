# Generated by Django 4.2.9 on 2024-05-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0024_remove_counselor_sessioncabin_counselor_sessioncabin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='afternoon_role',
        ),
        migrations.AddField(
            model_name='counselor',
            name='afternoon_role',
            field=models.ManyToManyField(blank=True, null=True, related_name='counselor_for_activity', to='afternoon_activity.afternoon_activity'),
        ),
    ]