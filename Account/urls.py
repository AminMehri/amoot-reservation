from django.urls import path
from Account import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', views.SignUp.as_view(), name='register'),
    path('', views.UserInfo.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sendVerifyEmail/', views.CreateEmailToken.as_view(), name='send-verify-email'),
    path('submitVerifyEmail/', views.VerifyEmail.as_view(), name='submit-verify-email'),
    path('forgetPassword/', views.ForgetPassword.as_view(), name='forget-password'),
    path('setPassword/', views.SetPassword.as_view(), name='set-password'),
]
