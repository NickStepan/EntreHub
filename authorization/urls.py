from django.urls import path
from .views import profile_view, edit_profile, index, register_view, login_view, logout_view

urlpatterns = [
    path('', index, name="index"),
    path('profile/<str:profile>', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]