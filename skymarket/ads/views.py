from rest_framework.filters import OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .filters import TitleSearchFilter
from .models import Ad, Comment
from .paginators import AdPagination
from .permissions import IsAllowed
from .serializers import AdSerializer, AdDetailSerializer, CommentSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    filterset_class = TitleSearchFilter
    ordering = ('-created_at',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        else:
            return AdSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAllowed]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class AdMeListAPIView(ListAPIView):
    serializer_class = AdSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    filterset_class = TitleSearchFilter
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = AdPagination

    def perform_create(self, serializer):
        ad_id = self.kwargs['ad_pk']
        ad = Ad.objects.get(pk=ad_id)
        serializer.save(author=self.request.user, ad=ad)

    def list(self, request, *args, **kwargs):
        ad_pk = self.kwargs.get('ad_pk')
        queryset = self.queryset.filter(ad_id=ad_pk)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def get_permissions(self):
        if self.action == ["retrieve", "create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAllowed]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
