# Generated by Django 5.0.3 on 2024-03-25 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0020_alter_assignment_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='submission',
            new_name='assignment',
        ),
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='file',
            new_name='submitted_file',
        ),
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='name',
        ),
    ]
