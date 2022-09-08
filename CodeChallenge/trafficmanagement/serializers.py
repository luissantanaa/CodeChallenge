from rest_framework import serializers
from .models import roadsegment
from django.contrib.auth.models import User


# Serializer for Road Segment objects
class RoadSegmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = roadsegment
		fields = ['ID', 'Long_start', 'Lat_start', 'Long_end', 'Lat_end', 'Length', 'Speed', 'Intensity',
				  'Characterization', 'Segment_start', 'Segment_end', 'Segment']


# Serializer for users
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']
