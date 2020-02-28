from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='ahome'),
    path('unpublished/',views.unpublished_news,name='aunpub'),
    path('unpublishedc/<str:cat>/',views.unpublished_category_news,name='aunpubcat'),
    path('unpublishedd/<str:d>/',views.unpublished_by_date,name='aunpubdate'),
    path('unpublisheddc/<str:d>/<str:cat>/',views.unpublished_by_date_category,name='aunpubdatecat'),
    path('published/',views.published_news,name='apub'),
    path('publishedc/<str:cat>/',views.published_category_news,name='apubcat'),
    path('publishedd/<str:d>/',views.published_by_date,name='apubdate'),
    path('publisheddc/<str:d>/<str:cat>/',views.published_by_date_category,name='apubdatecat'),
    path('delete/<int:nid>/',views.delete_news,name='adelnews'),
    path('publish/<int:nid>/',views.publish_news,name='apubnews'),
    path('detail/<int:nid>/',views.detail_news,name='adetnews'),
    path('editors/',views.editor_list,name='aelist'),
    path('edetail/<int:eid>/',views.editor_detail,name='aedetail'),
    path('eremove/<int:eid>/',views.editor_remove,name='aeremove'),
    path('enews/<int:eid>/',views.editor_news,name='aenews'),
    path('search/',views.search_news,name='asearch'),
    path('validate/<int:eid>/',views.validate_editor,name='aevalidate'),
    path('changepass/',views.change_password,name='achangepass'),
    path('report/',views.list_report,name='areport'),
    path('deleter/<int:rid>/',views.delete_report,name='adreport'),
    path('ignorer/<int:rid>/',views.ignore_report,name='aireport'),
]