from rest_framework import  permissions , status ,generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser , FormParser

from .auth_serializers import PasswordChangeSerializer , SignupSerializer , AccountSerializer

from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    POST /api/auth/signup/
    Creates a user and returns JWT tokens + user data.
    """
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request , *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "user" : AccountSerializer(user,context={"request": request}).data, 
            "tokens" :{
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)
    


class  ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/me/  -> returns current user
    PATCH /api/auth/me/ -> update profile (supports avatar upload)
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser , FormParser]

    def get_object(self):
        return self.request.user
    

# class PasswordChangeView(APIView):
#     """
#     POST /api/auth/signup/
#     Creates a user and returns JWT tokens + user data.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self , request , *args, **kwargs):
#         serializer = PasswordChangeSerializer(data = request.data ,context = {'request' : request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
    

class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

