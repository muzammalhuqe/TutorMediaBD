from django.urls import path, include
from . import views
urlpatterns = [
    path('singup/', views.UserRegistrationView.as_view(), name = 'singup'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('pass_change/', views.pass_change, name='passchange'),
]