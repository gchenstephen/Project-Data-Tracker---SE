# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='injectrate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='removerate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='iteration',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
    ]
