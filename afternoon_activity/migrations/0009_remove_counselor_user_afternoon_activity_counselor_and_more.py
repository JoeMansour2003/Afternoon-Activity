# Generated by Django 4.2.9 on 2024-05-09 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0008_remove_afternoon_activity_preference_in_range_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='user',
        ),
        migrations.AddField(
            model_name='afternoon_activity',
            name='counselor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counselor_for_activity', to='afternoon_activity.counselor'),
        ),
        migrations.AddField(
            model_name='counselor',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
