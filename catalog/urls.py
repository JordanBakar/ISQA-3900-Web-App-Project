from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
]
