# generic

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from bourseapp import models
from . import serializers
import operator
import functools

from rest_framework.permissions import IsAuthenticated

from drf_rw_serializers import generics, viewsets, mixins

from rest_framework.pagination import PageNumberPagination

"""
-- Category class --
"""


class CategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.CategorySerializer

    # permission_classes = []#[IsOwnerOrReadOnly]
    # queryset                = BlogPost.objects.all()

    # search, ?q=tt
    def get_queryset(self):
        qs = models.Category.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                # | Q(pic__icontains=query)
            ).distinct()

        query_list = self.request.GET.get("list")
        if query_list is not None:
            ls = query_list.split('_')
            for itm in ls:
                param = itm.split(':')
                itmId = param[0]
                itmVar = param[1]
                models.Category.objects.filter(pk=itmId).update(orderNum=itmVar)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get_serializer_context(self, *args, **kwargs):
    # return {"request": self.request}


class CategoryRudView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return models.Category.objects.all()

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)


class SymbolsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.SymbolSerializer

    # search, ?q=tt
    def get_queryset(self):
        qs = models.Company.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(symbol__startswith=query)
                # | Q(pic__icontains=query)
            ).distinct()

        return qs
