from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'property', PropertyViewSet, basename='property')
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]