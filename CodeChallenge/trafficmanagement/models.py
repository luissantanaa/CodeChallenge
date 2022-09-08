from django.contrib.gis.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Class defines the Road Segment model
class roadsegment(models.Model):

	# defines possible characterization choices
	Characterization_choices = [
		('High', 'High'),
		('Moderate', 'Moderate'),
		('Low', 'Low')
	]

	# defines possible intensity choices
	intensity_choices = [
		('2', '2'),
		('1', '1'),
		('0', '0')
	]

	# Road Segment Fields
	ID = models.AutoField(primary_key=True)
	Long_start = models.FloatField()
	Lat_start = models.FloatField()
	Long_end = models.FloatField()
	Lat_end = models.FloatField()
	Length = models.FloatField()
	Speed = models.FloatField()
	Intensity = models.CharField(max_length=1, choices=intensity_choices, default='99')
	Characterization = models.CharField(max_length=8, choices=Characterization_choices, default='default')
	Segment_start = models.PointField(blank=True, null=True)
	Segment_end = models.PointField(blank=True, null=True)
	Segment = models.LineStringField(blank=True, null=True)

# Function creates a token automatically for each user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)