from django.urls import path
from .views import UserProfileListView, UserProfileCreateView, UserProfileDetailView

urlpatterns = [
    path('profiles/', UserProfileListView.as_view(), name='profile-list'),
    path('profiles/create/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
]