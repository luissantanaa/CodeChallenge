"""TrafficManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from trafficmanagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('update/', views.update_database),
    path('roadsegments/', views.segment_list),  # list all segments
    path('addsegment/', views.add_segment),      # adds a segment
    path('segment/<int:id>', views.segment_info),  # shows segments details where segment.id == id
    path('updatesegment/<int:id>', views.update_segment_info),  # updates segment details where segment.id == id
    path('deletesegment/<int:id>', views.delete_segment), # deletes segment details where segment.id == id
    path('filteredintensitysegment/<str:intensity>', views.get_filtered_segments_by_intensity), # filters and lists segments where segment.intensity == intensity
    path('filteredcharacterizationsegment/<str:characterization>', views.get_filtered_segments_by_characterization), # filters and lists segments where segment.characterization == characterization
    path('api/token/auth/', views.CustomAuthToken.as_view()), # returns api auth token

]
