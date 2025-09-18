from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from .views import Home , ProjectViewSet , AttachmentViewSet ,CommentViewSet , TaskViewSet

router = DefaultRouter()
router.register(r'projects' , ProjectViewSet , basename='project')
router.register(r'tasks' , TaskViewSet , basename='task')
router.register(r'comments' , CommentViewSet , basename='comment')
router.register(r'attachments' , AttachmentViewSet , basename='attachements')


# urlpatterns = [
#     path('' , view=Home , name='home'),

# ]

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]