from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from app.serializers import UrlSerializer
from .models import Url
import string
import random
from rest_framework.response import Response


def random_url():
    """
    生成的範圍
    A~Z+a~z+0~9 共26+26+10=62個字符

    共有62**16種不同的短網址可生成
    """
    char=string.ascii_letters+string.digits
    return ''.join(random.choices(char,k=16))

def retrieve_url(request,short_url):
    url=get_object_or_404(Url,short_url=short_url)
    return redirect(url.origin_url)

class UrlAPIView(ModelViewSet):
    """
    Url產生API
    """
    serializer_class = UrlSerializer
    queryset = Url.objects.all()

    def create(self, request, *args, **kwargs):
        """創建一個Url object"""
        user_input=self.request.data.get('origin_url')
        exists_url=Url.objects.filter(origin_url=user_input).first()

        if exists_url:
            serializer=self.get_serializer(exists_url)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        random_short_url=random_url()

        for _ in range(5): #只嘗試5次 避免極端狀況產生
            try:
                result=Url.objects.create(origin_url=user_input,short_url=random_short_url)
                ans=self.get_serializer(result)
                return Response(ans.data,status=HTTP_201_CREATED)
            except IntegrityError: #產生的短網址已經存在 在重新產生一次
                random_short_url=random_url()
        return Response({'detail': 'Failed to generate a unique short URL after multiple attempts.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)