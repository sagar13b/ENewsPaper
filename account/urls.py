from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.surfer_signup,name='ssup'),
    path('esignup/',views.editor_signup,name='esup'),
    path('signin/',views.user_signin,name='sin'),
    path('signout/',views.user_signout,name='sut'),
]