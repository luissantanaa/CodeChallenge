import csv
import os

from django.contrib.gis.geos import LineString

from .models import roadsegment
from .serializers import RoadSegmentSerializer

from rest_framework.decorators import api_view
from rest_framework import status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


######################################################## GET REQUESTS #########################


# Reads "traffic_speed.csv", creates a Road Segment for each row of the file
@api_view(['GET'])
def update_database(request):
	segments = []

	print(os.path.dirname(os.path.abspath(__file__)) + "\\traffic_speed.csv")
	datareader = csv.DictReader(open(os.path.dirname(os.path.abspath(__file__)) + "/traffic_speed.csv"), delimiter=',')
	for row in datareader:
		intensity, characterization = characterize_traffic(float(row['Speed']))
		segment_start, segment_end, segment = create_segment_points(float(row['Lat_start']), float(row['Lat_end']),
																	float(row['Long_start']),
																	float(row['Long_end']))

		segments.append(roadsegment(Long_start=row['Long_start'], Lat_start=row['Lat_start'],
									Long_end=row['Long_end'],
									Lat_end=row['Lat_end'], Length=row['Length'], Speed=row['Speed'],
									Intensity=intensity, Characterization=characterization,
									Segment_start=segment_start, Segment_end=segment_end, Segment=segment))

	roadsegment.objects.bulk_create(segments)
	return Response("Data Imported", status=status.HTTP_201_CREATED)


# Gets all segments and lists them
@api_view(['GET'])
def segment_list(request):
	segments = roadsegment.objects.all()
	segmentSerializer = RoadSegmentSerializer(segments, many=True)
	return Response(segmentSerializer.data)


# Gets the segment whose id matches the one in the request and lists its details
@api_view(['GET'])
def segment_info(request, id):
	try:
		segment = roadsegment.objects.get(pk=id)  # checks if segment with given ID exists
	except roadsegment.DoesNotExist:
		return Response("No segment with given ID", status=status.HTTP_404_NOT_FOUND)

	serializer = RoadSegmentSerializer(segment)
	return Response(serializer.data)


# Filters the segments by intensity and lists the ones whose intensity matches the one in the request
@api_view(['GET'])
def get_filtered_segments_by_intensity(request, intensity):
	segments = roadsegment.objects.all().filter(Intensity=intensity)  # filters segments by their intensity
	serializer = RoadSegmentSerializer(segments, many=True)

	return Response(serializer.data, status=status.HTTP_200_OK)


# Filters the segments by characterization and lists the ones whose characterization matches the one in the request
@api_view(['GET'])
def get_filtered_segments_by_characterization(request, characterization):
	segments = roadsegment.objects.all().filter(
		Characterization=characterization)  # filters segments by their characterization
	serializer = RoadSegmentSerializer(segments, many=True)

	return Response(serializer.data, status=status.HTTP_200_OK)


######################################################## POST REQUESTS #########################


# Adds a Road Segment
@api_view(['POST'])
def add_segment(request):
	authentication_classes = [authentication.TokenAuthentication]  # Requires TokenAuthentication
	permission_classes = [permissions.IsAdminUser]  # Requires user to have admin permissions

	request.data["Intensity"], request.data["Characterization"] = characterize_traffic(
		request.data['Speed'])  # uses auxiliary function to characterize the segment based on speed

	request.data["segment_start"], request.data["segment_end"], request.data["segment"] = create_segment_points(
		request.data['Lat_start'], request.data['Lat_end'],
		request.data['Long_start'],
		request.data['Long_end'])

	serializer = RoadSegmentSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response("Added Road Segment", status=status.HTTP_201_CREATED)
	return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)



######################################################## PUT REQUESTS #########################


# Updates the segment, with the info received, whose id matches the one in the request
@api_view(['PUT'])
def update_segment_info(request, id):
	authentication_classes = [authentication.TokenAuthentication]  # Requires TokenAuthentication
	permission_classes = [permissions.IsAdminUser]  # Requires user to have admin permissions

	try:
		segment = roadsegment.objects.get(pk=id)  # checks if segment with given ID exists
	except roadsegment.DoesNotExist:
		return Response("No segment with given ID", status=status.HTTP_404_NOT_FOUND)

	serializer = RoadSegmentSerializer(segment, data=request.data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


######################################################## DELETE REQUESTS #########################


# Deletes the segment whose id matches the one in the request
@api_view(['DELETE'])
def delete_segment(request, id):
	authentication_classes = [authentication.TokenAuthentication]  # Requires TokenAuthentication
	permission_classes = [permissions.IsAdminUser]  # Requires user to have admin permissions

	try:
		segment = roadsegment.objects.get(pk=id)  # checks if segment with given ID exists
	except roadsegment.DoesNotExist:
		return Response("No segment with given ID", status=status.HTTP_404_NOT_FOUND)

	segment.delete()
	return Response("Segment deleted", status=status.HTTP_200_OK)


######################################################## Utilities #########################


# Auxiliary function used to characterize the segment based on its recorded speed
def characterize_traffic(speed):
	if speed <= 20:
		intensity = '2'
		characterization = "High"
	elif 20 < speed <= 50:
		intensity = '1'
		characterization = "Moderate"
	else:
		intensity = '0'
		characterization = "Low"

	return [intensity, characterization]


# Auxiliary function used to create the start and end points of the road segment.
# Then creates a LineString describing the road segment
def create_segment_points(lat_start, lat_end, long_start, long_end):
	segment_start = 'POINT(' + str(long_start) + ' ' + str(lat_start) + ')'
	segment_end = 'POINT(' + str(long_end) + ' ' + str(lat_end) + ')'
	segment = LineString((long_start, long_end), (lat_start, lat_end))

	return segment_start, segment_end, segment


# Auxiliary class used to return auth tokens
class CustomAuthToken(ObtainAuthToken):

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
										   context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'token': token.key,
			'user_id': user.pk,
			'email': user.email
		})
