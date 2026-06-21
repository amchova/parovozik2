from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cabinet/', views.user_dashboard, name='user_dashboard'),
    path('catalog/', views.catalog, name='catalog'),
    path('buy/<int:pk>/', views.buy_forecast, name='buy_forecast'),
    path('forecast/<int:pk>/', views.forecast_detail, name='forecast_detail'),
    path('admin-cabinet/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-cabinet/delete/<int:pk>/', views.delete_forecast, name='delete_forecast'),
]