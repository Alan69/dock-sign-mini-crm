from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('sign/', views.sign_document, name='sign_document'),
    path('doc-list', views.doc_list, name='doc_list'),
]
