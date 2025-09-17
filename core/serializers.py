from rest_framework import serializers
from .models import Project , Task , Attachment , Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ('id', 'username', 'display_name', 'avatar')


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