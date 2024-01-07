from django.urls import path, include
from . import views
from .views import home, contact, about, ProjectOne
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('project_one/', ProjectOne, name="project_one")
]

