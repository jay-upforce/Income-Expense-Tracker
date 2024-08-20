from django.urls import path
from User_app.views import UserCreateView, LoginView, UserDetailsView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),  # create a new user
    path('login/', LoginView.as_view(), name='user-login'), # login a user
    path('user/', UserDetailsView.as_view(), name='user-details'),   # logged-in user details (view, update, delete)
]
