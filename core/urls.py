from django.urls import path
from .views import Home

urlpatterns = [
    path('' , view=Home , name='home')
]
