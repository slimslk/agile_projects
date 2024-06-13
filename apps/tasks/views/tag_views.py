from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.tasks.models import Tag
from apps.tasks.serializers.tag_serializers import TagSerializer


class TagListAPIView(APIView):

    def get_objects(self):
        tags = Tag.objects.all()
        return tags

    def get(self, request: Request) -> Response:
        tags = self.get_objects()

        if not tags.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = TagSerializer(tags, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )