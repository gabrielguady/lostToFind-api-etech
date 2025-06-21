from rest_framework import viewsets, permissions
from core import models
from . import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username

        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import FileImageItem


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        item_type = request.data.get('item_type')  # 'lost' ou 'found'
        item_id = request.data.get('item_id')

        if not uploaded_file:
            return Response({"error": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)
        if item_type not in ['lost', 'found']:
            return Response({"error": "Tipo de item inválido. Use 'lost' ou 'found'."}, status=status.HTTP_400_BAD_REQUEST)
        if not item_id:
            return Response({"error": "ID do item não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = f"uploads/{uploaded_file.name}"
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        file_url = default_storage.url(saved_path)  # URL pública (se seu MinIO estiver configurado pra isso)

        # registro no banco
        file_image = FileImageItem.objects.create(
            filename=uploaded_file.name,
            remote_name=saved_path,
            lost_item_id=item_id if item_type == 'lost' else None,
            found_item_id=item_id if item_type == 'found' else None,
        )

        return Response({
            "id": file_image.id,
            "filename": file_image.filename,
            "remote_name": file_image.remote_name,
            "url": file_url,
        }, status=status.HTTP_201_CREATED)

