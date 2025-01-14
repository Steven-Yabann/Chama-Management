from django.urls import path, include
from .views.user_view import UserView
from .views.transaction_view import TransactionView
from .views.savings_view import SavingView
from .views.login_view import LoginView
from .views.register_view import RegisterView
from .views.logout_view import LogoutView
from .views.groups_view import CreateGroupView, JoinGroupView, GroupMembersView, GroupDetailsView, UserGroupsView
from .views.loan_view import LoanView, LoanRepaymentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer


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
    
    path('auth/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='Token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='Token_refresh_view'),

    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
    path('groups/join/', JoinGroupView.as_view(), name='join_group'),
    path('groups/<int:group_id>/details/', GroupDetailsView.as_view(), name='group_details'),
    path('groups/user/', UserGroupsView.as_view(), name='user_groups'),

    path('loans/', LoanView.as_view(), name='loan'),
    path('loans/<int:loan_id>/repay/', LoanRepaymentView.as_view(), name='loan_repayment'),
]