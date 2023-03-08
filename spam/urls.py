from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spam.views import ContactAPIView

router = DefaultRouter()
router.register('contact', ContactAPIView)

urlpatterns = [
    path('', include(router.urls))
]