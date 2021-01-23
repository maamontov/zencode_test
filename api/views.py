from rest_framework import viewsets, mixins

from api.models import Image, Comment, Like
from api.permissions import IsImageOwnerOrReadOnly, IsCommentOwnerOrReadOnly, \
    IsLikeOwnerOrReadOnly
from api.serializers import ImageSerializer, CommentSerializer, \
    LikeSerializer, CommentCreateUpdateDestroySerializer, \
    LikeCreateDestroySerializer, ImageCreateUpdateDestroySerializer


# region help
class CreateListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    pass
# endregion


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsImageOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return ImageCreateUpdateDestroySerializer
        return ImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(image=self.kwargs['image_pk'])

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return CommentCreateUpdateDestroySerializer
        return CommentSerializer


class LikeViewSet(CreateListViewSet):
    permission_classes = [IsLikeOwnerOrReadOnly]

    def get_queryset(self):
        return Like.objects.filter(image=self.kwargs['image_pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return LikeCreateDestroySerializer
        return LikeSerializer
