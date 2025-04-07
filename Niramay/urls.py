
from django.contrib import admin
from django.urls import path, include
from . import views
from remedies.views import filtered_remedies 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('remedies/', views.remedies, name='remedies'),
    path('filter-remedies/', views.filter_remedies, name="filter_remedies"),
    path('find-options/', views.find_options, name='find_options'),
    path('plants/', views.plants, name='plants'),  
    path('plants_features/<str:plant_name>/', views.plants_features, name='plants_features'),
    path('plants-info/', views.plants, name='plants'),
    path("recipes/", views.recipes_list, name="recipes"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('remedies/<int:severity_level>/', filtered_remedies, name='filtered_remedies'),
    path('filter-remedies/', views.filter_remedies, name="filter_remedies"),
    path('predict-plant/', views.predict_plant_view, name='predict_plant'),
    path('plant-details/<str:plant_name>/', views.plants_features, name='plants_features'),
    path('explore-plant/', views.plants_features_redirect, name='plants_features_redirect'),


]
