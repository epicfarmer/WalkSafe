# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=7, max_digits=9)),
                ('lon', models.DecimalField(decimal_places=7, max_digits=10)),
                ('update_date', models.DateTimeField(verbose_name='date last updated')),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('distance', models.PositiveIntegerField()),
                ('duration', models.DurationField()),
                ('update_date', models.DateTimeField(verbose_name='date last updated')),
                ('dst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coords_dst', to='directionsWithScores.Coordinates')),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coords_src', to='directionsWithScores.Coordinates')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='coordinates',
            unique_together=set([('lat', 'lon')]),
        ),
        migrations.AlterUniqueTogether(
            name='distance',
            unique_together=set([('src', 'dst')]),
        ),
    ]
