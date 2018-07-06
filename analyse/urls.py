from django.urls import path
from . import views

app_name = 'analyse'
urlpatterns = [
    path('app/list', views.app_list, name='app_list'),
    path('app/add', views.app_add, name='app_add'),
    path('app/not_exists', views.app_name_not_exists, name='app_name_not_exists'),
    path('app/edit/<int:id>', views.app_edit, name='edit_app'),

    path('field/list/<int:app_id>', views.field_list, name='field_list'),
    path('field/add/<int:app_id>', views.field_add, name='field_add'),
    path('field/name_not_exists/<int:app_id>', views.field_name_not_exists, name='field_name_not_exists'),
    path('field/key_not_exists/<int:app_id>', views.field_bind_name_not_exists, name='field_bind_name_not_exists'),
    path('field/edit/<int:id>', views.field_edit, name='field_edit'),
    path('field/change_index/<int:field_id>/<int:new_index>', views.field_change_index, name='field_change_index'),
]
