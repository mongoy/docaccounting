from django.urls import path
from django.contrib.auth import views


urlpatterns = [
    # Определенные ранее обработчики.
    # path('login/', views.user_login, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
