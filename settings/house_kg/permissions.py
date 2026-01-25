from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSellerForProperty(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.status == 'Seller'

class IsBuyerForReview(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.status == 'Buyer'