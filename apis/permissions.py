from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user


class PostPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return IsOwnerOrReadOnly().has_object_permission(request, view, obj)
        return True


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return IsOwnerOrReadOnly().has_object_permission(request, view, obj)
        return True
