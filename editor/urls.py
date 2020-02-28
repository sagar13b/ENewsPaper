from django.urls import path
from . import  views

urlpatterns = [
    path('home/',views.homepage,name='ehome'),
    path('create/',views.create_post,name='cpost'),
    path('myunews/',views.my_u_news,name='unews'),
    path('mypnews/',views.my_p_news,name='pnews'),
    path('ndetail/<int:nid>/',views.news_detail,name='endetail'),
    path('update/<int:nid>/',views.update_detail,name='updatenews'),
    path('delete/<int:nid>/',views.delete_post,name='deletenews'),
    path('news/<int:eid>/',views.all_news,name='allnews'),
    path('profile/',views.view_profile,name='eprofile'),
    path('updateprofile/',views.update_profile,name='eupdatep'),
    path('changepass/',views.change_password,name='echangepass'),
]