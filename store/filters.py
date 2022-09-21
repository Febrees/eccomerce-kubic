from re import search
import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    available = django_filters.BooleanFilter(field_name='available', lookup_expr='exact')
    search = django_filters.CharFilter(method='search_filter')

    class Meta:
        model = Product
        fields = ['category', 'available', 'search']
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
