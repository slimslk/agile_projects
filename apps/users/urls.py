from django.urls import path

from apps.users.views import UserListGenericView

urlpatterns = [
    path('', UserListGenericView.as_view()),
]
