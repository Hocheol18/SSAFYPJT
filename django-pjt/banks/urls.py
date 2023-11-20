from django.urls import path
from . import views

urlpatterns = [
    path('database/', views.deposit),
    path('savings/', views.saving),
    path('dview/', views.deposit),
    path('doview/', views.depositOptions),
    path('sview/', views.Saving),
    path('soview/', views.SavingOption),
]
