from django.urls import path

from jwtapp.views import (RegisterView, MySessionsView,
                           GetNewTokensView, LoginView,
                           SessionLogoutView, CloseSessionView,
                           CloseAllSessionsView)

urlpatterns = [

    path('api/v1/auth/generate_tokens/', GetNewTokensView.as_view()),

    path('api/v1/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/v1/auth/login/', LoginView.as_view()),

    path('api/v1/auth/sessions/my-sessions/', MySessionsView.as_view()),
    path('api/v1/auth/sessions/close/', CloseSessionView.as_view()),
    path('api/v1/auth/sessions/close-all/', CloseAllSessionsView.as_view()),
    path('api/v1/auth/sessions/log-out/', SessionLogoutView.as_view()),
]