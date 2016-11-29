from __future__ import unicode_literals

from django.db import models


class Coordinates(models.Model):
	# six decimal places is enough for 10cm accuracy
	lat = models.DecimalField(max_digits=9, decimal_places=7)
	lon = models.DecimalField(max_digits=10, decimal_places=7)
	update_date = models.DateTimeField('date last updated')


class Distance(models.Model):
	src = models.ForeignKey(Coordinates, related_name='coords_src', on_delete=models.CASCADE)
	dst = models.ForeignKey(Coordinates, related_name='coords_dst', on_delete=models.CASCADE)
	status = models.CharField(max_length=20)
	distance = models.PositiveIntegerField()
	duration = models.DurationField()  # With SQLite, big int field in microseconds
	update_date = models.DateTimeField('date last updated')
