# Generated by Django 5.0.3 on 2024-04-04 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0026_remove_assignmentsubmission_is_approve'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='is_approve',
            field=models.BooleanField(default=False),
        ),
    ]
