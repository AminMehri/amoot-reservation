from django.urls import path
from Account import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('register/', views.SignUp.as_view()),
    path('', views.UserInfo.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sendVerifyEmail/', views.CreateEmailToken.as_view()),
    path('submitVerifyEmail/', views.VerifyEmail.as_view()),
    path('forgetPassword/', views.ForgetPassword.as_view()),
    path('setPassword/', views.SetPassword.as_view()),
]
