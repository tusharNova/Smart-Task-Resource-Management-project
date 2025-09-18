from rest_framework import serializers 
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model , password_validation


User = get_user_model()

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('id' , 'username' , 'email' , 'display_name' , 'avatar')
        read_only_fields = ("id", "username")

    def update(self, instance, validated_data):

        return super().update(instance, validated_data)


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True ,required = True)
    password2 = serializers.CharField(write_only = True ,required = True)
    display_name = serializers.CharField(required = False , allow_blank = True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "display_name", "password", "password2")
        read_only_fields = ("id",)

    def validate(self, attrs):
        pw = attrs.get('password')
        pw2 = attrs.get('password2')
        if pw != pw2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        try:
            # temp_user = User(username = attrs.get('username') or "" , email = attrs.get('email') or "" )
            # password_validation.validate_password(password=pw, user=temp_user)
            temp_user = User(username=attrs.get("username") or "", email=attrs.get("email") or "")
            password_validation.validate_password(password=pw, user=temp_user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email", ""),
            display_name=validated_data.get("display_name", "")
        )
        user.set_password(password)
        user.save()
        return user
    

class PasswordChnageSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)


    def validate_old_password(self , value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    

    def validate(self, attrs):
        new_pw = attrs.get("new_password")
        new_pw2 = attrs.get("new_password2")
        if new_pw != new_pw2:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})
        
        try:
            password_validation.validate_password(password=new_pw, user=self.context["request"].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return attrs
       

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


    