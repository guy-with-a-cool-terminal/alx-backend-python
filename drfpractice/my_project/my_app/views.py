from django.shortcuts import render

from rest_framework import generics
from .models import *
from .serializers import *

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
