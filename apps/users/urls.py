from django.urls import path

from apps.users.views import UserListGenericView, RegisterUserGenericView

urlpatterns = [
    path('', UserListGenericView.as_view()),
    path('register/', RegisterUserGenericView.as_view()),
]
