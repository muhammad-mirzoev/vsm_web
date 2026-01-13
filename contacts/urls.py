from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contacts_list_view, name='list'),
    path('add/', views.send_request_view, name='add'),
    path('remove/<int:contact_id>/', views.remove_contact, name='remove'),
    path('accept/<int:pk>/', views.accept_request_view, name='accept'),
    path('reject/<int:pk>/', views.reject_request_view, name='reject'),
]
