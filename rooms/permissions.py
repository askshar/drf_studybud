from rest_framework import permissions


class IsHostOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Permission to allow only authenticated users to access this route.
        """
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Permission to allow only host user can update/delete own instances else only read.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.host == request.user
    

class MessagePermissions(IsHostOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
