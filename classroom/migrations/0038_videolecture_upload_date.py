# Generated by Django 5.0.3 on 2024-04-17 16:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0037_announcement_tutor_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolecture',
            name='upload_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
