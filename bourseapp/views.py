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

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from bourseapp.forms import SignUpForm


# first page
def index(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    news = models.News.objects.all()[0:10]
    targets = models.Targets.objects.all()

    # if request.user.is_authenticated:
    return render(request, 'bourseapp/index.html', {
        'news': news,
        'targets': targets,
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
    search = request.GET.get('search', '')
    category_id = request.GET.get('category_id', -1)

    companies = models.Company.objects.filter((Q(symbol__icontains=search)
                                              | Q(fullName__icontains=search)
                                              | Q(bourseType__icontains=search)
                                              | Q(createAt__icontains=search)
                                              | Q(description__icontains=search))
                                              & Q(category=category_id)
                                              )


    search_category = request.GET.get('search-category', '')

    categories = models.Category.objects.filter(Q(title__icontains=search_category)
                                                | Q(createAt__icontains=search_category)
                                                | Q(description__icontains=search_category)
                                                )

    # return render(request, 'bourseapp/company_list.html', {
    return render(request, 'bourseapp/symbols_list.html', {
        'categories': categories,
        'companies': companies,
        'search': search,
        'search_category': search_category,
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


@user_passes_test(lambda u: u.is_superuser)
def technical_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    technical = models.Technical.objects.filter(Q(company__symbol__icontains=search)
                                      | Q(createAt__icontains=search)
                                      | Q(description__icontains=search)
                                      )
    paginator = Paginator(technical, page_size)
    try:
        technical = paginator.page(page)
    except PageNotAnInteger:
        technical = paginator.page(1)
    except EmptyPage:
        technical = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/technical_list.html', {
        'technical': technical,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def fundamental_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    fundamentals = models.Fundamental.objects.filter(Q(company__symbol__icontains=search)
                                      | Q(createAt__icontains=search)
                                      | Q(description__icontains=search)
                                      )
    paginator = Paginator(fundamentals, page_size)
    try:
        fundamentals = paginator.page(page)
    except PageNotAnInteger:
        fundamentals = paginator.page(1)
    except EmptyPage:
        fundamentals = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/fundamental_list.html', {
        'fundamentals': fundamentals,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def targets_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    targets = models.Targets.objects.filter(Q(company__symbol__icontains=search)
                                      | Q(createAt__icontains=search)
                                      | Q(description__icontains=search)
                                      )
    paginator = Paginator(targets, page_size)
    try:
        targets = paginator.page(page)
    except PageNotAnInteger:
        targets = paginator.page(1)
    except EmptyPage:
        targets = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/targets_list.html', {
        'targets': targets,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def category_detail(request, category_id):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    companies = models.Company.objects.filter((Q(symbol__icontains=search)
                                              | Q(fullName__icontains=search)
                                              | Q(bourseType__icontains=search)
                                              | Q(createAt__icontains=search)
                                              | Q(description__icontains=search))
                                              & Q(category=category_id)
                                              )
    category = models.Category.objects.get(id=category_id)
    paginator = Paginator(companies, page_size)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/category_detail.html', {
        'category': category,
        'companies': companies,
        'search': search,
        'page_size': page_size
    })


@user_passes_test(lambda u: u.is_superuser)
def company_detail(request, company_id):
    company = get_object_or_404(models.Company, pk=company_id)
    news = models.News.objects.filter(company=company.id)
    technicals = models.Technical.objects.filter(company=company.id)
    fundamental = models.Fundamental.objects.filter(company=company.id)
    return render(request, 'bourseapp/compay_detail.html', {
        'company': company,
        'news': news,
        'technicals': technicals,
        'fundamentals': fundamental,
    })


@user_passes_test(lambda u: u.is_superuser)
def news_detail(request, news_id):
    news = get_object_or_404(models.News, pk=news_id)
    return render(request, 'bourseapp/news_detail.html', {
        'news': news,
    })


@user_passes_test(lambda u: u.is_superuser)
def technical_detail(request, technical_id):
    technical = get_object_or_404(models.Technical, pk=technical_id)
    return render(request, 'bourseapp/technical_detail.html', {
        'technical': technical,
    })


@user_passes_test(lambda u: u.is_superuser)
def fundamental_detail(request, fundamental_id):
    fundamental = get_object_or_404(models.Fundamental, pk=fundamental_id)
    return render(request, 'bourseapp/fundamental_detail.html', {
        'fundamental': fundamental,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'registration/admin_user_confirmation.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
