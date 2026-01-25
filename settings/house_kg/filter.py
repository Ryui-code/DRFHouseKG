from django_filters import FilterSet
from .models import Property, UserProfile

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'property_type': ['exact'],
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'price': ['gt', 'lt'],
            'floor': ['gt', 'lt'],
            'total_floors': ['gt', 'lt'],
            'area': ['gt', 'lt'],
            'rooms': ['exact'],
            'condition': ['exact'],
            'created_date': ['gt', 'lt'],
        }

class UserFilterSet(FilterSet):
    class Meta:
        model = UserProfile
        fields = [
            'username'
        ]