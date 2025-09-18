from rest_framework import serializers
from .models import Project , Task , Attachment , Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'display_name', 'avatar')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'uploaded_at')


class CommentSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = ('id' , 'task' , 'author' , 'text' , 'created_at')
        read_only_fields = ('author' , 'created_at')


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserBriefSerializer(read_only = True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        write_only = True , queryset = User.objects.all() , source = 'assignee', required = False ,allow_null = True
    ) 

    attachment = AttachmentSerializer(many = True , read_only = True)
    comment = CommentSerializer(many = True , read_only = True)

    class Meta:
        model = Task
        fields = (
            'id' , 'project' , 'title' , 'descriptions' , 'assignee' ,'assignee_id' ,'status' , 'priority' , 'due_date' ,'attachment','comment' ,'watchers', 'created_at' , 'updated_at' 
        )


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only = True)
    owner_id = serializers.PrimaryKeyRelatedField(
        write_only = True , queryset = User.objects.all() , source = 'owner', required = False ,allow_null = True
    )
    member = UserBriefSerializer(read_only = True , many = True)
    member_id = serializers.PrimaryKeyRelatedField(
        write_only = True , queryset = User.objects.all() , source = 'member', required = False ,allow_null = True
    )

    tasks = Task(many = True , read_only = True)

    class Meta:
        model = Project
        fields = (
            'id' , 'name' ,'descriptions' , 'owner' , 'owner_id' , 'member' , 'member_id' ,'task' ,  'created_at' , 'updated_at'
        )
        read_only_feilds = ('created_at' , 'updated_at' , 'owner' , 'members' , 'tasks')
