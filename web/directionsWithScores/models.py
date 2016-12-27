from __future__ import unicode_literals

from django.db import models


class Coordinates(models.Model):

	PLACES = 7

	# six decimal places is enough for 10cm accuracy
	lat = models.DecimalField(max_digits=9, decimal_places=PLACES)
	lon = models.DecimalField(max_digits=10, decimal_places=PLACES)
	update_date = models.DateTimeField('date last updated', auto_now=True)

	@staticmethod
	def round(value):
		import decimal
		if value is None:
			raise ValueError

		if not isinstance(value, decimal.Decimal):
			value = decimal.Decimal(value)

		return value.quantize(decimal.Decimal('0.1') ** Coordinates.PLACES)

	def __lt__(self, other):
		if self.lat < other.lat:
			return True
		elif self.lat == other.lat:
			return self.lon < other.lon
		else:
			return False

	def __gt__(self, other):
		if self.lat > other.lat:
			return True
		elif self.lat == other.lat:
			return self.lon > other.lon
		else:
			return False


	class Meta:
		unique_together = ("lat", "lon")
		index_together = ("lat", "lon")


class Distance(models.Model):
	src = models.ForeignKey(Coordinates, related_name='coords_src', on_delete=models.CASCADE)
	dst = models.ForeignKey(Coordinates, related_name='coords_dst', on_delete=models.CASCADE)
	status = models.CharField(max_length=20)
	distance = models.PositiveIntegerField()
	duration = models.DurationField()  # With SQLite, big int field in microseconds
	update_date = models.DateTimeField('date last updated')

	class Meta:
		unique_together = ("src", "dst")
		index_together = ("src", "dst")
