# Generated by Django 5.0.3 on 2024-03-25 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0023_remove_assignment_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='status',
        ),
    ]