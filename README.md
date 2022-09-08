# CodeChallenge

The code in this repository contains a Rest Api for managing traffic in several road segments. The project was built using Django, and uses the mdillon/postgis Docker image as the database.

To execute the app go to CodeChallenge/CodeChallenge and execute command "docker-compose up". This command sould start the application and create the docker container.
After the application is running use the '/update/' endpoint to populate the database. To use the provided Postman collection the user must first select if he wants admin access or not. First we require an authentication token, to get this we use the endpoint 'api/token/auth/'. To get admin acess use the "Get Token (Admin)" request, copy the returned token and then paste it in the headers section of the requests you which to execute. If the user wants guest access then he would run "Get Token (User)". Admin access is required to execute any non-GET requests.  

### Endpoints  
  'admin/' - Used to access the django admin page  
  'update/' - Used to populate the database with the info in "traffic_speed.csv"  
  'roadsegments/' - Returns a list containg all the road segment objects present in the database  
  'addsegment/' - Adds a road segment object to the database  
  'segment/<int:id>' - Returns the information of the segment whose id matches the one in the url  
  'updatesegment/<int:id>' - Updates the information of the segment whose id matches the one in the url with data contained in the request  
  'deletesegment/<int:id>' - Deletes the road segment whose id matches the one in the url   
  'filteredintensitysegment/<str:intensity>' - Returns a list of road segment objects whose intensity match the one in the url  
  'filteredcharacterizationsegment/<str:characterization>' - Returns a list of road segment objects whose characterization match the one in the url  
  'api/token/auth/' - Returns an auth token to access the api via Postman  
  
### Docker-Compose  

```
version: "3.9"

services:
  web:
    build: .
    command: >
      bash -c "python manage.py runserver 0.0.0.0:8000
      && python manage.py startup"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: mdillon/postgis:latest
    environment:
      - POSTGRES_DB=postgis
      - POSTGRES_USER=postgis
      - POSTGRES_PASSWORD=postgis
    restart: on-failure
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
```

Service web refers to the Django application. This will run the server on localhost:8000 and execute the startup script (documented below).  
Service db refers to the postgis docker image. This image will serve as the database for the application.  

### Dockerfile  

```
FROM python:3.8
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
COPY . /code/
```

The dockerfile contains instructions to install the requirements for the project and to install the gdal-bin package which is used with postgis.  

### Startup  
```
import psycopg2
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Command script used to create the project Database, make migrations, migrate and load the users present in users.json

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #self.createDB()
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "users.json")
```

This script runs several "python manage.py" commands. The first to refer to the migrations required by the database. The third one loads the data from the file "users.json". This file contains information regarding two users of the django app, one with admin access and a guest. This allows us to create users automatically on startup.  

### Views  

The views.py file contains several methods which are executed when you call the endpoints.  
  
   'update_database' - Reads 'traffic_speed.csv', iterates through the rows of the file and creates several road segment objects. The method also calculates the intensity and characterization of traffic based on the average speed. It also calculates the start point, end point and the segment that the object represents.  
   'segment_list' - Returns a list containing all road segment objects.  
   'segment_info' - Receives an id and returns the information regarding the road segment whose id matches the one received.  
   'get_filtered_segments_by_intensity' - Receives an intensity value and returns all road segments whose intensity matches the one received.  
   'get_filtered_segments_by_characterization' - Receives an characterization value and returns all road segments whose characterization matches the one received.  
   'add_segment' - Adds a road segment object with the data in the request. The method also calculates the intensity and characterization of traffic based on the average speed. It also calculates the start point, end point and the segment that the object represents.  
   'update_segment_info' - Updates the information regarding the road segment whose id matches the one received.  
   'delete_segment' - Deletes the road segment whose id matches the one received.  
   'characterize_traffic' - Auxiliary function used to calculate the intensity and characterization based on average speed.  
   'create_segment_points' - Auxiliary function used to create the start and end points of the segment, and also the segment itself.  
   'CustomAuthToken' - Auxiliary class used to return auth tokens.  
   
   
   


