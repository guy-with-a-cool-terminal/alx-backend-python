import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter messages by conversation participant username
    user = django_filters.CharFilter(field_name='conversation__participants__username', lookup_expr='icontains')

    # Filter messages by date range
    date_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'date_after', 'date_before']
