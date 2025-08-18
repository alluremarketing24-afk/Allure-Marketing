from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('videos/type/<int:type_id>/', views.get_videos_by_type, name='videos_by_type'),
    
    # ✅ Add this line for AJAX contact submission
    path('contact_ajax/', views.contact_ajax, name='contact_ajax'),
    
    # Custom Admin Panel
    path('pops/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('pops/videos/', views.custom_admin_videos, name='custom_admin_videos'),
    path('pops/contacts/', views.custom_admin_contacts, name='custom_admin_contacts'),
    path('pops/services/', views.custom_admin_services, name='custom_admin_services'),
    path('pops/contacts/export/', views.export_contacts_excel, name='export_contacts_excel'),
    
]



