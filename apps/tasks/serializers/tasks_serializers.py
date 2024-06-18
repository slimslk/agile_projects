from rest_framework import serializers
from apps.tasks.models import Task


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    assignee = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Task
        fields = ('name', 'status', 'priority', 'project', 'assignee', 'deadline')


