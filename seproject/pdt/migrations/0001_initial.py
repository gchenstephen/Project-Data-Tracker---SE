# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('which_iteration', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('implementation', models.CharField(default='Bad fix', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeveloperSession',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sloc', models.PositiveIntegerField(default=0, verbose_name='Iteration SLOC')),
                ('sloc_ppm', models.PositiveIntegerField(default=0, verbose_name='SLOC per person-month by iteration')),
                ('start_date', models.DateTimeField(verbose_name='Start date', null=True)),
                ('finish_date', models.DateTimeField(blank=True, verbose_name='Finish date', null=True)),
                ('status', models.BooleanField(default=False, verbose_name='Iteration completed')),
                ('effort', models.PositiveIntegerField(default=0, verbose_name='Iteration effort')),
                ('defect_count', models.PositiveIntegerField(default=0, verbose_name='Iteration defect count')),
                ('goodfix_count', models.PositiveIntegerField(default=0)),
                ('defect_density', models.FloatField(default=0)),
                ('devno', models.PositiveIntegerField(default=0)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('injectrate', models.FloatField(default=0)),
                ('removerate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sloc', models.PositiveIntegerField(default=0, verbose_name='Phase SLOC')),
                ('sloc_ppm', models.PositiveIntegerField(default=0, verbose_name='SLOC per person-month by phase')),
                ('coun', models.PositiveIntegerField(default=0, verbose_name='Iteration count')),
                ('status', models.BooleanField(default=False, verbose_name='Project completed')),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name='Start date')),
                ('finish_date', models.DateTimeField(blank=True, verbose_name='Finish date', null=True)),
                ('effort', models.PositiveIntegerField(default=0, verbose_name='Phase effort')),
                ('defect_count', models.PositiveIntegerField(default=0, verbose_name='Defect count')),
                ('goodfix_count', models.PositiveIntegerField(default=0)),
                ('defect_density', models.FloatField(default=1)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('injectrate', models.FloatField(default=0)),
                ('removerate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False, verbose_name='Project completed')),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name='Start date')),
                ('finish_date', models.DateTimeField(blank=True, verbose_name='Finish date', null=True)),
                ('sloc', models.PositiveIntegerField(default=0, verbose_name='Iteration count')),
                ('duration', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(auto_now=True, verbose_name='start time')),
                ('resume_time', models.DateTimeField(auto_now=True, verbose_name='resume time')),
                ('end_time', models.DateTimeField(blank=True, verbose_name='end time', null=True)),
                ('total_time', models.PositiveIntegerField(default=0, verbose_name='total time(in seconds)')),
                ('modified_time', models.PositiveIntegerField(default=0, verbose_name='modified time(in seconds)')),
                ('developer', models.ForeignKey(to='pdt.Developer')),
                ('iteration', models.ForeignKey(to='pdt.Iteration')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='phase',
            field=models.ForeignKey(to='pdt.Phase'),
        ),
        migrations.AddField(
            model_name='developer',
            name='iteration',
            field=models.ForeignKey(null=True, to='pdt.Iteration'),
        ),
        migrations.AddField(
            model_name='defect',
            name='developer',
            field=models.ForeignKey(to='pdt.Developer'),
        ),
        migrations.AddField(
            model_name='defect',
            name='iteration',
            field=models.ForeignKey(to='pdt.Iteration'),
        ),
    ]
