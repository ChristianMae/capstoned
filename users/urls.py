from django.urls import path, include
from users.views import (
    SignUpView,
    VerifyTokenView,
    # LoginView,
    LogoutView,
    VerifyEmailView
    )

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_token/<str:token>/', VerifyTokenView.as_view(), name='verify_token'),
    path('verify_email/', VerifyEmailView.as_view(), name='verify_email')
]