from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserGetSerializer, UserSerializer, ImageSerializer, UserProfileSerializer, UserPasswordSerializer
from django.db.models import Q
from django.core.files.storage import default_storage
from cloudinary.models import CloudinaryResource
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url
import cloudinary


@api_view(['GET'])
def endpoints(request):
    data = ['/users', '/users/:username', '/users/:username/avatar', '/users/:username/password']
    return Response(data)


class UserList(APIView):
    # def has_permission(self, request, view):
        # return bool(request.user and request.user.is_superuser)

    def get(self, request):
        query = request.GET.get('query', '')
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )[0:5]
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self):
        User.objects.all().delete()
        return Response(status=204)


class ManagerList(APIView):

    def get(self, request):
        managers = User.objects.filter(is_staff=True)
        serializer = UserGetSerializer(managers, many=True)
        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
class UserDetail(APIView):
    def get_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        if request.user.username != username and not request.user.is_superuser:
            return Response(status=403)
        
        user = self.get_object(username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return Response(status=204)

class ManagerProfile(APIView):
    def get_object(self, id):
        return get_object_or_404(User, id=id)

    def get(self, request, id):
        manager = self.get_object(id)
        serializer = UserProfileSerializer(manager)
        data = {
            "first_name": serializer.data["first_name"],
            "last_name": serializer.data["last_name"],
            "avatar": serializer.data["avatar"],
            "number_of_homestays": manager.homestay_set.count()
        }
        return Response(data)


@permission_classes([IsAuthenticated])
class UserUpdateAvatar(APIView):

    def put(self, request, username):
        serializer = ImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = get_object_or_404(User, username=username)

        # Remove old avatar if it exists
        if user.avatar:
            public_id = user.avatar.public_id
            destroy(public_id)

        # Upload new avatar
        image = serializer.validated_data.get('image')
        upload_result = upload(image, folder='homestay-renting-website/user_avatars')
        url, options = cloudinary_url(upload_result['public_id'],
                                      format=upload_result['format'])
        userSerializer = UserProfileSerializer(user, data={"avatar": url}, partial=True)
        if not userSerializer.is_valid():
            return Response(userSerializer.errors, status=400)
        userSerializer.save()

        return Response(userSerializer.data, status=200)

@permission_classes([IsAuthenticated])
class UserUpdatePassword(APIView):
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserPasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)