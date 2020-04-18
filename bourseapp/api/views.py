# generic

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from bourseapp import models
from . import serializers
import operator
import functools
import pandas as pd

from rest_framework.permissions import IsAuthenticated

from drf_rw_serializers import generics, viewsets, mixins

from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse

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

        query_category = self.request.GET.get("c")
        if query_category is not None:
            qs = qs.filter(
                Q(category=query_category)
            ).distinct()

        return qs


def chart_detail(request, company_id):
    chart = get_object_or_404(models.Chart, company=company_id)
    print('chart')
    print(chart)
    if chart.data is not None:
        print('data valid')
        # read the file
        df = pd.read_csv(chart.data)
        print(df.head())

        profile_json = {
            # "Date": df['<DTYYYYMMDD>'].to_json(orient='values'),
            # "Close": df['<CLOSE>'].to_json(orient='values'),
            "data": df.to_json(),
        }
    else:
        print('data invalid')  # read the file

        profile_json = {
            "data": "empty",
        }
    return JsonResponse(profile_json, safe=False)


def ChartView(request):

    chart = get_object_or_404(models.Chart, company__symbol__icontains='شاخص بازار بورس')
    if chart.data is not None:
        print('data valid')
        # read the file
        df = pd.read_csv(chart.data)
        # print(df.head())

        profile_json = {
            # "Date": df['<DTYYYYMMDD>'].to_json(orient='values'),
            # "Close": df['<CLOSE>'].to_json(orient='values'),
            "data": df.to_json(),
        }
    else:
        print('data invalid')# read the file

        profile_json = {
            "data": "empty",
        }
    return JsonResponse(profile_json, safe=False)



