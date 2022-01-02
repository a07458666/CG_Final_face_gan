from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('cycleGan/', views.cycle_gan, name='cycle_gan'),
]