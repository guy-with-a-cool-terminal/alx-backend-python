from rest_framework import serializers
from .models import Book
from datetime import datetime
from django.utils.timezone import now

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def get_days_since_created(self,obj):
        return (now() - obj.created_at).days
    