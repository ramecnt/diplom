from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .apps import SalesConfig
from . import views

app_name = SalesConfig.name

ad_router = SimpleRouter()
ad_router.register(prefix=r'ads', viewset=views.AdViewSet, basename='ads')
comment_router = SimpleRouter()
comment_router.register(prefix=r'comments', viewset=views.CommentViewSet, basename='comments')

urlpatterns = [
    path('api/ads/me/', views.AdMeListAPIView.as_view(), name='list_ad_me'),
    path('api/', include(ad_router.urls)),
    path('api/ads/<int:ad_pk>/', include(comment_router.urls), name='comments'),
]