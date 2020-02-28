from django.urls import path
from . import views

urlpatterns = [
    path('news/<int:pk>/',views.News.as_view()),
    path('news/',views.NewsList1.as_view()),
]