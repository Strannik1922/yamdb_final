from rest_framework import permissions


def check_post(request):
    return (request.method == 'POST'
            and (request.user.is_user
                 or request.user.is_moderator
                 or request.user.is_admin))


def check_patch_delete(request, obj):
    methods = ['PATCH', 'DELETE']
    return (request.method in methods
            and (request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author))


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_authenticated and request.user.is_admin)


class StaffOrAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or (request.user.is_authenticated
                    and (check_patch_delete(request, obj)
                         or check_post(request))))


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser or request.user.is_authenticated
                and request.user.is_admin)
