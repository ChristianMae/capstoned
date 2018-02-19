from django.urls import path, include
from users.views import (
    SignUpView,
    VerifyTokenView,
    LogoutView,
    VerifyEmailView,
    TermsAndConditionView,
    )

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_token/<str:token>/', VerifyTokenView.as_view(), name='verify_token'),
    path('verify_email/', VerifyEmailView.as_view(), name='verify_email'),
    path('terms/', TermsAndConditionView.as_view(), name='tac')
]