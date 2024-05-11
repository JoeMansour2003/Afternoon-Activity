# Generated by Django 4.2.9 on 2024-05-11 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afternoon_activity', '0019_remove_camper_cabin_camper_session_cabin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camper',
            name='session_cabin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cabin_for_camper', to='afternoon_activity.sessioncabin'),
        ),
    ]
