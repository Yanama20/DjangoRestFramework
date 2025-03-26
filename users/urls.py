from django.urls import path
from users.views import AuthAPIView, RegistrationAPIView, ConfirmAPIView

urlpatterns = [
    path('registration/', AuthAPIView.as_view()),
    path('authorization/', RegistrationAPIView.as_view()),
    path('confirm/', ConfirmAPIView.as_view()),
    path('authorization_cbv/', AuthAPIView.as_view()),
    path('registration_cbv/', RegistrationAPIView.as_view()),
    path('confirm_cbv/', ConfirmAPIView.as_view()),
]