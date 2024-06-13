from django.urls import path
from apps.tasks.views.tag_views import TagListAPIView, TagDetailApiView

urlpatterns = [
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:tag_id>', TagDetailApiView.as_view())
]