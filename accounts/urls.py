from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_panel/', views.adminPanel, name='admin_panel'),
    path('contact/', views.contact, name='contact'),
    path('prices/', views.prices, name='prices'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('create_user/', views.usercreation, name='register'),
    path('create_role/', views.createRole, name='create_role'),
    path('create_bundle/', views.createBundle, name='create_bundle'),
    path('delete_user/<str:pk>/', views.deleteUser, name='delete_user'),
    path('create_appointment/', views.add_appointments, name='create_appointment'),
    path('update_role/<str:pk>/', views.updateRole, name='update_role'),
    path('update_user/<str:pk>/', views.updateUser, name='update_user'),
    path('update_bundle/<str:pk>/', views.updateBundle, name='update_bundle'),
    path('delete_role/<str:pk>/', views.deleteRole, name='delete_role'),
    path('delete_bundle/<str:pk>/', views.deleteBundle, name='delete_bundle'),
    path('show_role/', views.showRole, name='show_role'),
    path('show_bundle/', views.showBundle, name='show_bundle'),
    path('view_profile/<str:pk>/', views.singleProfile, name='single_profile'),
]

