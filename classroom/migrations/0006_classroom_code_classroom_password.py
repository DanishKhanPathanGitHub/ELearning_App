# Generated by Django 5.0.3 on 2024-03-24 02:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0005_classroom_cover_pic_classroom_students_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='code',
            field=models.IntegerField(default=123456, max_length=9, validators=[django.core.validators.MinLengthValidator(6)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classroom',
            name='password',
            field=models.CharField(default='danish@123456789', max_length=20),
            preserve_default=False,
        ),
    ]