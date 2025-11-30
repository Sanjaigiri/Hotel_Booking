from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
  
    path("signup/", views.signup, name="signup"),
    path("signup/verify/", views.signup_verify, name="signup_verify"),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # OTP verification endpoints
    path('booking/request-otp/', views.request_otp_view, name='request_otp'),
    path('booking/verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('booking/payment/', views.payment_view, name='payment'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]