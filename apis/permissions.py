from django.shortcuts import render
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.user == request.user:
            return True
        return False

class CanCreatePostOrComment(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True
        return False

class CanLikePostOrComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if obj.user != request.user:
            return True
        return False