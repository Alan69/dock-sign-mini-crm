from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('sign/', views.sign_document, name='sign_document'),
    path('doc-list', views.doc_list, name='doc_list'),
    path('my_docksigngroups/', views.user_docksigngroups, name='user_docksigngroups'),
    path('create_docksigngroup/', views.create_docksigngroup, name='create_docksigngroup'),
    path('docksigngroup/<int:pk>/', views.docksigngroup_detail, name='docksigngroup_detail'),
]
