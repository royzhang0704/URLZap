from rest_framework.routers import DefaultRouter

from . import views
from django.urls import path, include


router=DefaultRouter()
router.register('url',views.UrlAPIView,basename='url')
urlpatterns=[
    path('',include(router.urls)),
    path('<str:short_url>/',views.retrieve_url)
]