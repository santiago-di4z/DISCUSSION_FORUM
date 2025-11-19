from django.urls import path
from .views import reg_view, lin_view, lout_view

urlpatterns = [
    path('register/', reg_view, name='register'),
    path('login/', lin_view, name='login'),
    path('logout/', lout_view, name='logout'),
]