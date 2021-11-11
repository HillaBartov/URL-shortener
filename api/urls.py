from django.contrib import admin
from django.urls import path
# from rest_framework import routers
from api import views
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path('create/', views.CreateShorterViewSet.as_view(), name="create"),
    path('s/<slug:short>', views.RedirectShorterViewSet.as_view(), name="short"),
]
