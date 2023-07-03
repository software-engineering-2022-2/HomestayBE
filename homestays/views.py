from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Homestay
from .serializers import HomestaySerializer
from django.db.models import Q



class ListHomestays(APIView):

    def get(self, request):
        query = request.GET.get('query', '')
        homestays = Homestay.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) 
        )
        serializer = HomestaySerializer(homestays, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HomestaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self):
        Homestay.objects.all().delete()
        return Response(status=204)


@permission_classes([IsAuthenticated])
class HomestayDetail(APIView):
    def get_object(self, name):
        return get_object_or_404(Homestay, name=name)

    def get(self, request, name):
        homestay = self.get_object(name)
        serializer = HomestaySerializer(homestay)
        return Response(serializer.data)

    def put(self, request, name):
        homestay = self.get_object(name)
        serializer = HomestaySerializer(homestay, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, name):
        homestay = self.get_object(name)
        homestay.delete()
        return Response(status=204)
