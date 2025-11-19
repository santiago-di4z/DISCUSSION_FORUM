from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('board/<str:short_name>/', views.board_detail, name='board_detail'),
    path('board/<str:short_name>/new-thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/comment/', views.create_comment, name='create_comment'),
]