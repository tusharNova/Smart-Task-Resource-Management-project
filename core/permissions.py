from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    """
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj , 'owner'):
            return obj.owner == request.user

        if hasattr(obj , 'project'):
            if obj.project.owner == request.user:
                return True
            
            if obj.assignee and obj.assignee ==request.user:
                return True

        return False