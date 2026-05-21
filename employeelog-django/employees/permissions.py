from rest_framework import permissions
from .models import Company

class IsCompanyAdmin(permissions.BasePermission):
    """
    Allow access only to authenticated company admins for objects in their company.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Company):
            return obj == request.user.company
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return False

class IsCompanyManager(permissions.BasePermission):
    """
    Allow access to admins and managers for objects in their company.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admin', 'manager'])

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Company):
            return obj == request.user.company
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return False

class IsCompanyEmployee(permissions.BasePermission):
    """
    Allow access to any authenticated company user for objects in their company.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Company):
            return obj == request.user.company
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return False

class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    """
    Read-only for all company users, write for admin only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Company):
            return obj == request.user.company
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return False

class IsCompanyAdminOrManagerOrReadOnly(permissions.BasePermission):
    """
    Read-only for employees/managers/admins.
    Update for admins/managers.
    Create/Delete for admins only.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Read operations
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Create operation: only admins
        if request.method == 'POST':
            return request.user.role == 'admin'
            
        # Update/delete operations: check role in has_object_permission or here
        return request.user.role in ['admin', 'manager']

    def has_object_permission(self, request, view, obj):
        # Enforce tenant isolation first
        is_same_tenant = False
        if isinstance(obj, Company):
            is_same_tenant = (obj == request.user.company)
        elif hasattr(obj, 'company'):
            is_same_tenant = (obj.company == request.user.company)
            
        if not is_same_tenant:
            return False
            
        # Deletion: only admins
        if request.method == 'DELETE':
            return request.user.role == 'admin'
            
        # Updating: admins and managers
        if request.method in ['PUT', 'PATCH']:
            return request.user.role in ['admin', 'manager']
            
        return True
