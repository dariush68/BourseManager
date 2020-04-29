# generic

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination

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

        query_category = self.request.GET.get("c")
        if query_category is not None:
            qs = qs.filter(
                Q(category=query_category)
            ).distinct()

        return qs


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserList(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]  # [IsOwnerOrReadOnly, IsAuthenticated]
    # pagination_class = StandardResultsSetPagination

    # search, ?q=tt
    def get_queryset(self):
        qs = User.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(username__icontains=query)
            ).distinct()

        return qs[:20]


class ChatMessageAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ChatMessageSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    # search, ?q=tt
    def get_queryset(self):
        qs = models.ChatMessage.objects.all()
        # limit msgs
        if self.request.user.groups.filter(name='level1').exists() is False and self.request.user.is_superuser is False:
            qs = qs.filter(
                Q(receiver=self.request.user) | Q(sender=self.request.user)
            ).distinct()

        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(description__icontains=query)
                # | Q(pic__icontains=query)
            ).distinct()

        query_target = self.request.GET.get("target")
        if query_target is not None:
            qs = qs.filter(
                (Q(receiver=query_target) & Q(sender=self.request.user))
                |
                (Q(receiver=self.request.user) & Q(sender=query_target))
            ).distinct()

        query_user2admin = self.request.GET.get("user2admin")
        query_admin = self.request.GET.get("admin")
        if query_user2admin is not None and query_admin is not None:
            qs = qs.filter(
                (Q(receiver=query_user2admin) & Q(sender=query_admin))
                |
                (Q(receiver=query_admin) & Q(sender=query_user2admin))
            ).distinct()

        return qs

    def perform_create(self, serializer):
        # serializer.save(sender=self.request.user)
        serializer.save()
        # tick all unseen messages
        if get_user_model().objects.get(id=self.request.data['sender']).username == 'admins':
            user_reciver = get_user_model().objects.get(id=self.request.data['receiver'])
            unReadMsg = models.ChatMessage.objects.filter(Q(sender=user_reciver) & Q(isSeen=False))
            unReadMsg.update(isSeen=True)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get_serializer_context(self, *args, **kwargs):
    # return {"request": self.request}


class ChatMessageRudView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ChatMessageSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return models.ChatMessage.objects.all()

