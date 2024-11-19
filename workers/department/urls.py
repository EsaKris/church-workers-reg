from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('worker/', views.worker_user, name='worker'),
    path('success/', views.success_view, name='success'),
    path('worker-cards/', views.worker_cards, name='worker_cards'),  # Add this path
    path('worker/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    path('record-attendance/', views.record_attendance, name='record_attendance'),  # Corrected: Added 'views.'
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
