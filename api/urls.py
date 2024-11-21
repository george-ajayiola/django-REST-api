from django.urls import path, include
from . import views


urlpatterns = [
    path('drinks/',views.drinks_list),
    path('drinks/<str:name>',views.drink_detail),
    path('health/',views.health),
]
