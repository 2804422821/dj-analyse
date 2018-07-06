from django.urls import path
from . import views

app_name = 'data'
urlpatterns = [
    path('list', views.data_list, name='data_list'),
    path('record/<int:app_id>', views.data_record, name='data_record'),
]
