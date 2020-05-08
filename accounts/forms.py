from django.forms import ModelForm

from . models import *


class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
