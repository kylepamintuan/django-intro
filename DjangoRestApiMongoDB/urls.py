
from django.conf.urls import url, include
import subprocess

urlpatterns = [
    url(r'^', include('users.urls')),
]
