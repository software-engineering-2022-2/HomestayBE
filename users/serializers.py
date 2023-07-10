from django.contrib.auth.hashers import make_password, check_password
from rest_framework.serializers import ModelSerializer, BaseSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value: str) -> str:
        return make_password(value)

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )
    
    def validate_username(self, username):
        if username != self.instance.username:
            raise serializers.ValidationError('Username not match')
        return username

class UserPasswordSerializer(ModelSerializer):
    new_password = serializers.CharField(max_length=512, write_only = True)
    password = serializers.CharField(max_length=512, write_only = True)
    class Meta:
        model = User
        fields = ["username", "password", "new_password"]
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.pop('password')
        new_password = attrs.get('new_password')

        if username != self.instance.username:
            raise serializers.ValidationError('Username not match')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username')
        
        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid old password')
        
        if password == new_password:
            raise serializers.ValidationError('Password should be different')

        attrs['password'] = make_password(new_password)
        return attrs
 

class ImageSerializer(BaseSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    def to_internal_value(self, data):
        img = data.get('image')
        if not img:
            raise serializers.ValidationError({
                'image': 'This field is required.'
            })
        return {
            'image': img
        }

    def to_representation(self, instance):
        return {}
    