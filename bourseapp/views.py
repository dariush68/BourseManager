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
    categories = models.Category.objects.all()
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
