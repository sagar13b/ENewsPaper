from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='shome'),
    path('detail/<int:nid>/',views.detail_news, name='sndetail'),
    path('comment/<int:nid>/',views.comment_news,name='sncom'),
    path('like/<int:nid>/',views.like_news,name='snlike'),
    path('reply/<int:cid>/',views.comment_comment,name='sccom'),
    path('category/<str:cat>/',views.category_news,name='scat'),
    path('date/<str:date>/',views.date_by_news,name='sdat'),
    path('date/<str:date>/<str:cat>/',views.date_category_news,name='scatdat'),
    path('eprofile/<int:eid>/',views.editor_profile,name='seprofile'),
    path('follow/<int:eid>/',views.follow_editor,name='sfeditor'),
    path('subscribtion/',views.subscribtion,name='sesuscribe'),
    path('subscribtion/<int:eid>/',views.subscribtion_editor,name='sesuscriben'),
    path('search/',views.search_news,name='ssearch'),
    path('asearch/',views.advance_search_news,name='sasearch'),
    path('notification/',views.show_notification,name='snotification'),
    path('report/<int:cid>/<str:val>/,',views.report_comment,name='sreport'),
    path('example/',views.example,name='e'),
]