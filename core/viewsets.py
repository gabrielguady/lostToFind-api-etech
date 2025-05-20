from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from core import serializers, filters, models, serializers_params, behaviors


class FileImageViewSet(viewsets.ModelViewSet):
    queryset = models.FileImageItem.objects.all()
    serializer_class = serializers.FileImageSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtendo os parâmetros da requisição
        item_id = self.request.query_params.get('item_id')  # ID do LostItem ou FoundItem
        item_type = self.request.query_params.get('item_type')  # 'lost' ou 'found'

        if item_id and item_type:
            if item_type == 'lost':
                # Filtra as imagens associadas ao LostItem com o ID fornecido
                queryset = queryset.filter(lost_item__id=item_id)
            elif item_type == 'found':
                # Filtra as imagens associadas ao FoundItem com o ID fornecido
                queryset = queryset.filter(found_item__id=item_id)
            else:
                # Caso item_type não seja nem 'lost' nem 'found', retorna queryset vazio
                queryset = queryset.none()

        return queryset


class LostItemViewSet(viewsets.ModelViewSet):
    queryset = models.LostItem.objects.all()
    serializer_class = serializers.LostItemSerializer
    filterset_class = filters.LostItemFilter
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False, parser_classes=[MultiPartParser])
    def upload_file(self, request, *args, **kwargs):
        serializer = serializers_params.FileImageItemSerializerParam(data=request.data)
        serializer.is_valid(raise_exception=True)

        behavior = behaviors.MediaViewBehavior(**serializer.validated_data, type_item='lost_item')
        response = behavior.run()

        return Response(data=response, status=status.HTTP_201_CREATED)


class FoundItemViewSet(viewsets.ModelViewSet):
    queryset = models.FoundItem.objects.all()
    serializer_class = serializers.FoundItemSerializer
    filterset_class = filters.FoundItemFilter
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False, parser_classes=[MultiPartParser])
    def upload_file(self, request, *args, **kwargs):
        serializer = serializers_params.FileImageItemSerializerParam(data=request.data)
        serializer.is_valid(raise_exception=True)

        behavior = behaviors.MediaViewBehavior(**serializer.validated_data, type_item='found_item')
        response = behavior.run()

        return Response(data=response, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryItemSerializer
    filterset_class = filters.ItemCategoryFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]