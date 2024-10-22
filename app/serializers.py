from rest_framework import serializers
from .models import Url

class UrlSerializer(serializers.ModelSerializer):
    """序列化網址"""
    class Meta:
        model=Url
        fields="__all__"
        read_only_fields=['short_url','created_at']
