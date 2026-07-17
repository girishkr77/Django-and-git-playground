from rest_framework import permissions

class IsadminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.is_staff)
    
class Fulldjangomodelpermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] =  ['%(app_label)s.view_%(model_name)s']

class Viewhistoryofcustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
        