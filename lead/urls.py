from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from . import views


app_name = 'leads'
urlpatterns = [
    path('', views.home, name='lead'),
]
