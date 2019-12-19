from django.db.models import Q
# from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from mypy.test import update
from django.db.models import Q

from bourseapp import models

# from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import ModelForm

from django.db.models import CharField, Value
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Sum

from jalali_date import datetime2jalali, date2jalali


# first page
def index(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    # if request.user.is_authenticated:
    return render(request, 'bourseapp/index.html', {
    })

    # HttpResponseRedirect(reverse('admin:login'))


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def category_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    categories = models.Category.objects.filter(Q(title__icontains=search)
                                                | Q(createAt__icontains=search)
                                                | Q(description__icontains=search)
                                                )
    paginator = Paginator(categories, page_size)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/category_list.html', {
        'categories': categories,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def company_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    companies = models.Company.objects.filter(Q(symbol__icontains=search)
                                              | Q(fullName__icontains=search)
                                              | Q(category__title__icontains=search)
                                              | Q(bourseType__icontains=search)
                                              | Q(createAt__icontains=search)
                                              | Q(description__icontains=search)
                                              )
    paginator = Paginator(companies, page_size)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/company_list.html', {
        'companies': companies,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def new_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    news = models.News.objects.filter(Q(title__icontains=search)
                                      | Q(company__symbol__icontains=search)
                                      | Q(reference__icontains=search)
                                      | Q(createAt__icontains=search)
                                      | Q(tag__icontains=search)
                                      | Q(description__icontains=search)
                                      )
    paginator = Paginator(news, page_size)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/new_list.html', {
        'newss': news,
        'search': search,
        'page_size': page_size
    })
