from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('create-request/', views.create_request, name='create_request'),
    path('create-query/', views.create_query, name='create_query'),
    path('approve-company/<int:company_id>/', views.approve_company, name='approve_company'),
    path('complete-request/<int:request_id>/', views.complete_request, name='complete_request'),
    path('resolve-query/<int:query_id>/', views.resolve_query, name='resolve_query'),
]
