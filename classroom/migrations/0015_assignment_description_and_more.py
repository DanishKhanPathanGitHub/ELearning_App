# Generated by Django 5.0.3 on 2024-03-25 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0014_announcement_assignment_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='file',
            field=models.FileField(null=True, upload_to='class/assignments_submissions'),
        ),
    ]
