from django.urls import path

from jwtapp.views import (RegisterView, MySessionsView,
                           RefreshTokenView, LoginView,
                           SessionLogoutView, CloseSessionView,
                           CloseAllSessionsView, CloseSessionByCredentialsView,
                           ResetPasswordView, CheckVerificationCodeView,
                           ChangeProfilePhotoView)

urlpatterns = [


    path('api/v1/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/v1/auth/login/', LoginView.as_view()),
    path('api/v1/auth/refresh-token/', RefreshTokenView.as_view()),
    path('api/v1/auth/password-reset/', ResetPasswordView.as_view()),
    path('api/v1/auth/check-verification-code/', CheckVerificationCodeView.as_view()),

    path('api/v1/auth/sessions/my-sessions/', MySessionsView.as_view()),
    path('api/v1/auth/sessions/close/', CloseSessionView.as_view()),
    path('api/v1/auth/sessions/close-all/', CloseAllSessionsView.as_view()),
    path('api/v1/auth/sessions/close-by-credentials/', CloseSessionByCredentialsView.as_view()),
    path('api/v1/auth/sessions/log-out/', SessionLogoutView.as_view()),

    path('api/v1/change_profile_photo/', ChangeProfilePhotoView.as_view())
    
]