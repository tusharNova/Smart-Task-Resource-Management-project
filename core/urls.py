from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from .views import Home , ProjectViewSet , AttachmentViewSet ,CommentViewSet , TaskViewSet

from .auth_views import SignupView , ProfileView , PasswordChangeView 

router = DefaultRouter()
router.register(r'projects' , ProjectViewSet , basename='project')
router.register(r'tasks' , TaskViewSet , basename='task')
router.register(r'comments' , CommentViewSet , basename='comment')
router.register(r'attachments' , AttachmentViewSet , basename='attachements')


# urlpatterns = [
#     path('' , view=Home , name='home'),

# ]

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("auth/signup", SignupView.as_view(), name="auth-signup"),
    path("auth/me/", ProfileView.as_view(), name="auth-me"),
    path("auth/change-password/", PasswordChangeView.as_view(), name="password-change"),

    path('', include(router.urls)),
]