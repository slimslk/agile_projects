from django.urls import path

from apps.projects.views.project_views import ProjectListAPIView


urlpatterns = [
    path('', ProjectListAPIView.as_view())
]
