# ine_mongodb_api
API using INE data ingested into MongoDB with ETL

### Deployment steps

**Localhost:**
To deploy, run:
```
docker-compose up --build
```

## DESCRIPTION

Next, it will be described the steps for the deployment script. 


### Create a new project for our API

```
django-admin startproject api
```

### Create a new app for our API

```
cd api

python3 manage.py startapp ine
```

### Register app with the project

#### api/settings.py
```
INSTALLED_APPS = [
    'ine.apps.IneConfig',
    ... # Leave all the other INSTALLED_APPS
]
```

### Migrate the database
```
python3 manage.py migrate
```

### Set Database

#### api/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'CLIENT': {
            "host": "mongodb://root:mongoadmin@mongo:27017/",
            "name": "ine",
        }
    }
}
```

### Create Super User
```
python3 manage.py createsuperuser

Username: admin
Email address: admin@admin.com
Password: admin
```

### Create models in the database
#### ine/models.py
```
from django.db import models
from jsonfield import JSONField

import uuid

# Create your models here.
class dict_ccaa(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CODAUTO = models.CharField(max_length=2)
    NOMBRE = models.CharField(max_length=50)


class dict_provinces(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CPRO = models.CharField(max_length=2)
    NOMBRE = models.CharField(max_length=50)


class dict_municipalities(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CODAUTO = models.CharField(max_length=2)
    CPRO = models.CharField(max_length=2)
    CMUN = models.CharField(max_length=3)
    DC = models.CharField(max_length=1)
    NOMBRE = models.CharField(max_length=50)


class metadata(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=2)
    collections = JSONField()
    description = models.CharField(max_length=999)
    current_data = models.CharField(max_length=10)
    published_data = models.CharField(max_length=10)
```

### Register data with the admin site
#### ine/admin.py
```
from django.contrib import admin
from ine.models import dict_ccaa, dict_provinces, dict_municipalities, metadata

admin.site.register(dict_ccaa)
admin.site.register(dict_provinces)
admin.site.register(dict_municipalities)
admin.site.register(metadata)
```

### Set up Django REST Framework
#### api/settings.py
```
INSTALLED_APPS = [
    # All your installed apps stay the same
    ...
    'rest_framework',
]
```

### Serialize the model
#### Create serializers.py
```
> ine/serializers.py
```

```
from rest_framework import serializers
from ine.models import dict_ccaa, dict_provinces, dict_municipalities

class dict_ccaa_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_ccaa
        fields = ('CODAUTO', 'NOMBRE')

class dict_provinces_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_provinces
        fields = ('CPRO', 'NOMBRE')

class dict_municipalities_Serializer(serializers.ModelSerializer):
    class Meta:
        model = dict_municipalities
        fields = ('CODAUTO', 'CPRO', 'CMUN', 'DC', 'NOMBRE')
```

### Views
#### ine/views.py:
```
from ine.models import dict_ccaa, dict_provinces, dict_municipalities
from ine.serializers import dict_ccaa_Serializer, dict_provinces_Serializer, dict_municipalities_Serializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class dict_ccaa_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        ccaa = dict_ccaa.objects.all()
        serializer = dict_ccaa_Serializer(ccaa, many=True)
        return Response(serializer.data)


class ccaa_Detail(APIView):

    def get_object(self, codauto):
        try:
            return dict_ccaa.objects.get(CODAUTO=codauto)
        except dict_ccaa.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a CA.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Andalucía
        """
        ccaa = self.get_object(nombre)
        serializer = dict_ccaa_Serializer(ccaa)
        return Response(serializer.data)


class dict_provinces_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        provinces = dict_provinces.objects.all()
        serializer = dict_provinces_Serializer(provinces, many=True)
        return Response(serializer.data)


class provinces_Detail(APIView):

    def get_object(self, cpro):
        try:
            return dict_provinces.objects.get(CPRO=cpro)
        except dict_provinces.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a province.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Cádiz
        """
        provinces = self.get_object(nombre)
        serializer = dict_provinces_Serializer(provinces)
        return Response(serializer.data)


class dict_municipalities_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        municipalities = dict_municipalities.objects.all()
        serializer = dict_municipalities_Serializer(municipalities, many=True)
        return Response(serializer.data)


class municipalities_Detail(APIView):

    def get_object(self, nombre):
        try:
            return dict_municipalities.objects.get(NOMBRE=nombre)
        except dict_municipalities.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a municipalitie.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Jerez de la Frontera
        """
        municipalities = self.get_object(nombre)
        serializer = dict_municipalities_Serializer(municipalities)
        return Response(serializer.data)
```

### Site URLs
#### api/urls.py
```
from django.urls import path

from django.conf.urls import include

urlpatterns = [
    path('', include('ine.urls')),
]
```

### API URLs
#### ine/urls.py
```
> ine/urls.py
```
```
from django.contrib import admin
from django.urls import path
from ine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ccaa/list/', views.dict_ccaa_List.as_view()),
    path('ccaa/<str:nombre>/', views.ccaa_Detail.as_view()),
    path('provinces/list/', views.dict_provinces_List.as_view()),
    path('provinces/<str:nombre>/', views.provinces_Detail.as_view()),
    path('municipalities/list/', views.dict_municipalities_List.as_view()),
    path('municipalities/<str:nombre>/', views.municipalities_Detail.as_view()),
]
```

### SWAGGER
#### api/settings.py
```
INSTALLED_APPS = [
    ...
    'drf_yasg',
    ...
]
```

#### api/urls.py
```
...
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="INE API",
      default_version='v1',
      description="Get INE DATA",
      terms_of_service="https://www.ine.com/policies/terms/",
      contact=openapi.Contact(email="contact@bmat.local"),
      license=openapi.License(name="INE License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    ...
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```

### Make migrations
```
python manage.py makemigrations
```

### Migrate the Database
```
python manage.py migrate
```

### Start up Django's development server
```
python manage.py runserver
```


## Docker commands


List all containers, stop and remove
```
docker ps -aq
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker container prune
```

List images and remove
```
docker images -a
docker rmi $(docker images -q)
docker images prune -a
```