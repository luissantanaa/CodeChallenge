from django.contrib import admin
from .models import roadsegment

# Registers the model in order to be able to see the data in admin page
admin.site.register(roadsegment)

# Defines the details to show in admin page
class RoadSegmentAdmin(admin.ModelAdmin):
	list_display = ['ID', 'Long_start', 'Lat_start', 'Long_end', 'Lat_end', 'Length', 'Speed', 'Segment_Start', 'Segment_End', 'Segment']
