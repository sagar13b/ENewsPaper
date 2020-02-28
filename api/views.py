#Rest Framework fields
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .permissions import ReadOnly, IsEditor
from .serializers import NewsSerializer
from editor.models import NewsPost
# Create your views here.
class NewsList(APIView):
    def get(self, request, pk):
        nl = NewsPost.objects.get(id=pk)
        seriali = NewsSerializer(nl)
        return Response(seriali.data)

    def post(self, request, pk):
        n = NewsPost()
        seriali = NewsSerializer(n,data=request.data)
        if seriali.is_valid():
            seriali.save()
            return Response(seriali.data)
        else:
            return Response(seriali.error)

class NewsList1(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    queryset = NewsPost.objects.all()
    permission_classes = [IsAuthenticated|ReadOnly]

class News(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = NewsPost.objects.all()
    permission_classes = [IsEditor|ReadOnly]