from rest_framework.permissions import BasePermission
from account.models import User

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return False

class IsEditor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.editor_detail == request.user:
            return True
        else:
            return False