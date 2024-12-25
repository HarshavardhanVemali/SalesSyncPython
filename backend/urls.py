from django.contrib import admin
from django.urls import path,include
import api
import api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
