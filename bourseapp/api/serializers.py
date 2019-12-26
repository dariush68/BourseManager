from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
import json
from django.core.serializers.json import DjangoJSONEncoder

from bourseapp import models


class CategorySerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Category
        fields = [
            'url',
            'id',
            'user',
            'title',
            'pic',
            'date',
            'orderNum',
        ]
        read_only_fields = ['id', 'user', 'date', 'url']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = models.Category.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value


class SymbolSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = models.Company
        fields = [
            'id',
            'symbol',
            'fullName',
            'bourseType',
            'tse',
            'site',
            'isTarget',
            'category',
        ]
        read_only_fields = ['id', 'symbol', 'fullName', 'bourseType', 'tse', 'site', 'isTarget']

