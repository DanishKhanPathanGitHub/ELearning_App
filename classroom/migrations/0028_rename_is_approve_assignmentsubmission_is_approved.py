# Generated by Django 5.0.3 on 2024-04-04 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0027_assignmentsubmission_is_approve'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='is_approve',
            new_name='is_approved',
        ),
    ]
