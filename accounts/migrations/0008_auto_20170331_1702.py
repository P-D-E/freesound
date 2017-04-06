# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-31 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20170328_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailpreferencetype',
            name='send_by_default',
            field=models.BooleanField(default=True, help_text=b'Indicates if the user should receive an email, if UserEmailSetting exists for the user then the behavior is the opposite'),
        ),
    ]