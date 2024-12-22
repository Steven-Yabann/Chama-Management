from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user_view import UserView
from .views.transaction_view import TransactionView
from .views.savings_view import SavingView
from .views.login_view import LoginView
from .views.register_view import RegisterView
from .views.logout_view import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/user/<int:id>/', UserView.as_view()),
    
    path('savings/', SavingView.as_view()),
    path('savings/user/<int:user_id>/', SavingView.as_view()),
    
    path('transactions/', TransactionView.as_view()),
    path('transactions/user/<int:user_id>/', TransactionView.as_view()),
    
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    path('auth/token/', TokenObtainPairView.as_view(), name='Token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='Token_refresh_view')
]