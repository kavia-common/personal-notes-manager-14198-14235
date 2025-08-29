from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, register, login_view, logout_view, NoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('', include(router.urls)),
]
