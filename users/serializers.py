from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from users.models import ConfirmationCode



class UserBasicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=55)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserAuthSerializer(UserBasicSerializer):
    pass    

class UserRegisterSerializer(UserBasicSerializer):
    def validate_user(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists')

class UserConfirmSerializer(UserBasicSerializer):
    code = serializers.CharField(max_length=6)
    class Meta:
        model = ConfirmationCode
        fields = ['code']
    def validate_confirmation_code(self, code):
        try:
            ConfirmationCode.objects.get(code=code)
        except:
            raise ValidationError('Invalid confirmation code')
        return code
    
    def activate_user(self,code):
        user_id = ConfirmationCode.objects.get(code=code).user.id
        user = User.objects.get(id=user_id)
        if user:
            user.is_active = True
            user.save()
        else:
            raise ValidationError('No such user')
        