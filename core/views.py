from django.shortcuts import render , HttpResponse
from rest_framework import viewsets , permissions , status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from django.shortcuts import get_list_or_404  

from .models import User , Attachment , Comment , Task , Project

from .serializers import UserBriefSerializer  ,CommentSerializer , TaskSerializer , ProjectSerializer ,AttachmentSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model

def Home(request):
    return HttpResponse("<h1>hey user</h1>")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('member' , 'owner').all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated , IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend , SearchFilter ,OrderingFilter)
    filter_fields =('owner' , 'member')
    search_fields = ('name' , 'descriptions') 
    ordering_fields = ('created_at','updated_at')


    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


    @action(detail=True , methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        project.members.add(user)
        return Response({'status':'member added'}, status=status.HTTP_200_OK)
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('project','assignee').all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('project','status','assignee','priority')
    search_fields = ('title','description')
    ordering_fields = ('due_date','priority','created_at')

    def perform_create(self, serializer):
        # ensure created by an authenticated user; you can add extra logic
        serializer.save()

    @action(detail=True, methods=['post'])
    def add_watcher(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        task.watchers.add(user)
        return Response({'status':'watcher added'})
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author','task').all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related('task').all().order_by('-uploaded_at')
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
