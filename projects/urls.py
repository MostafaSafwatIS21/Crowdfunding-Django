from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='list'),
    path('create/', views.project_create_view, name='create'),
    path('<int:id>/', views.project_detail_view, name='detail'),
    path('<int:id>/edit/', views.project_edit_view, name='edit'),
    path('<int:id>/delete/', views.project_delete_view, name='delete'),
    path('<int:id>/fund/', views.fund_project, name='fund'),
]
