from django.urls import path

from apps.projects.views.project_views import ProjectListAPIView, ProjectDetailAPIView


urlpatterns = [
    path('', ProjectListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view())
]
