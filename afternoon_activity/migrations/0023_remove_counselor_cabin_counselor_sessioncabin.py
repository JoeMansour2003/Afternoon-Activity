# Generated by Django 4.2.9 on 2024-05-13 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0022_remove_activity_activity_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='cabin',
        ),
        migrations.AddField(
            model_name='counselor',
            name='sessionCabin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counselors_cabin', to='afternoon_activity.sessioncabin'),
        ),
    ]
