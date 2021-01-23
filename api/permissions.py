from rest_framework import permissions

from api.models import Image, Comment, Like


class IsOwnerOrReadOnly(permissions.BasePermission):
    entity = None

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        if self.entity is not None:
            obj = self.entity.objects.get(pk=view.kwargs['pk'])
            return request.user == obj.user
        return False


class IsImageOwnerOrReadOnly(IsOwnerOrReadOnly):
    entity = Image


class IsCommentOwnerOrReadOnly(IsOwnerOrReadOnly):
    entity = Comment


class IsLikeOwnerOrReadOnly(IsOwnerOrReadOnly):
    entity = Like
