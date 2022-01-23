import django_filters
from django.forms import TextInput
from .forms import DateInput
from .models import Sighting


class SightingFilter(django_filters.FilterSet):
    Port = django_filters.CharFilter(widget=TextInput(attrs={'class': 'form-control form-control-lg '
                                                                      'secondary-text-color'}),
                                     field_name='Port', label='Port Name', lookup_expr='icontains')

    Date = django_filters.DateFilter(widget=DateInput(attrs={'class': 'form-control form-control-lg '
                                                                      'secondary-text-color'}),
                                     field_name='Date',
                                     lookup_expr='gte', label='Sighting Date')

    class Meta:
        model = Sighting
        fields = [
            'Port',
            'Date',
            'First_Species_Observed',
        ]
