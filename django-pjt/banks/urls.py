from django.urls import path
from . import views

urlpatterns = [
    path('database/', views.deposit),
    path('savings/', views.savings),
    path('dview/', views.deposit),
    path('doview/', views.depositOptions),
    path('sview/', views.saving),
    path('soview/', views.SavingOption),
]
