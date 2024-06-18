from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404

from apps.projects.models import Project
from apps.projects.serializers.project_file_serializers import CreateProjectFileSerializer


class ProjectFileListGenericView(ListCreateAPIView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        file = request.FILES.get("file", None)
        project_id = request.data.get("project_id", None)
        request.data["file_name"] = file.name if file else None
        project = get_object_or_404(Project, project_id)
        context = {
            "file": file,
            "project": project
        }
        serializer = CreateProjectFileSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )