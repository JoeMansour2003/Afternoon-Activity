# Generated by Django 4.2.9 on 2024-05-09 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0009_remove_counselor_user_afternoon_activity_counselor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afternoon_activity',
            name='counselor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counselor_for_activity', to='afternoon_activity.counselor'),
        ),
    ]
