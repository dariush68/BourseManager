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
from django.contrib.auth import get_user_model

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Sum

from jalali_date import datetime2jalali, date2jalali

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from bourseapp.forms import SignUpForm, NewsForm
from django.db.models import Count
from django.http import HttpResponse


# first page
from bourseapp.models import Technical
tutorialCategory = models.TutorialCategory.objects.all()


def index(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    news = models.News.objects.all()[0:20]
    technicals = models.Technical.objects.all().exclude(user__username='d_abedi') # [0:10]
    technicals_count = technicals.count()

    fundamentals = models.Fundamental.objects.all()[0:20]
    bazaar = models.Bazaar.objects.all()[0:10]
    webinar = models.Webinar.objects.all()[0:10]
    targets = models.Company.objects.filter(isTarget=True)
    messages = models.Message.objects.filter(isShow=True)
    tutorials = models.Tutorial.objects.all()[0:12]
    comp_tech = models.Technical.objects.all().values_list('company__id')
    comp_fund = models.Fundamental.objects.all().values_list('company__id')
    comp_bazr = models.Bazaar.objects.all().values_list('company__id')
    comp_analiz = comp_tech.union(comp_fund)
    comp_analiz = comp_analiz.union(comp_bazr)
    all_analized_symbols = models.Company.objects.filter(id__in=comp_analiz)

    itms = models.Technical.objects.filter(user__username='d_abedi').values_list('company__id')
    target_watch = models.Company.objects.filter(id__in=itms)

    # filter latest technical for display in home
    technical_proseced_list = []
    technical_target_list = []
    technical_vip_target_list = []

    # remove repeated same symbol from list
    for itm in technicals:
        if itm.isSuperUserPermition:
            technical_vip_target_list.append(itm)
        else:
            if itm.company.id in technical_proseced_list:
                pass
            elif itm.company.isTarget:
                technical_proseced_list.append(itm.company.id)
                technical_target_list.append(itm)

    # remove repeated same vip symbol from list
    technical_vip_target_list2 = []
    technical_vip_target_list_id = []
    for itm in technical_vip_target_list:
        if itm.company.id in technical_vip_target_list_id:
            pass
        else:
            technical_vip_target_list2.append(itm)
            technical_vip_target_list_id.append(itm.company.id)

    for itm in technical_target_list:
        technical_vip_target_list2.append(itm)

    users_inactive_count = get_user_model().objects.filter(is_active=False).count()
    news_inactive_count = models.News.objects.filter(isApproved=False).count()
    events = (users_inactive_count + news_inactive_count)
    users_count = get_user_model().objects.all().count()

    # if request.user.is_authenticated:
    return render(request, 'bourseapp/index.html', {
        # return render(request, 'bourseapp/test.html', {
        'news': news,
        'targets': targets,
        'bazaars': bazaar,
        'webinar': webinar,
        'technicals': technical_vip_target_list2[0:20],
        'technicals_count': technicals_count,
        'fundamentals': fundamentals,
        'messages': messages,
        'targets_watch': target_watch,
        'tutorials': tutorials,
        'tutorialCategory': tutorialCategory,
        'all_analized_symbols': all_analized_symbols,
        'users_inactive_count': users_inactive_count,
        'news_inactive_count': news_inactive_count,
        'events': events,
        'users_count': users_count,
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
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def manager_panel(request):

    users = get_user_model().objects.all().order_by('groups')
    users_inactive = get_user_model().objects.filter(is_active=False)
    news_inactive = models.News.objects.filter(isApproved=False)
    events = (users_inactive.count() + news_inactive.count())

    return render(request, 'bourseapp/manager_panel.html', {
        'users': users,
        'users_inactive': users_inactive,
        'news_inactive': news_inactive,
        'events': events,
    })


@login_required
# @user_passes_test(lambda u: u.is_superuser)
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
    return render(request, 'bourseapp/symbols/symbols_list.html', {
        'categories': categories,
        'companies': companies,
        'search': search,
        'search_category': search_category,
        'tutorialCategory': tutorialCategory,
    })


@login_required
# @user_passes_test(lambda u: u.is_superuser)
def company_analyzed(request):

    comp_tech = models.Technical.objects.all().values_list('company__id')
    comp_fund = models.Fundamental.objects.all().values_list('company__id')
    comp_bazr = models.Bazaar.objects.all().values_list('company__id')
    comp_analiz = comp_tech.union(comp_fund)
    comp_analiz = comp_analiz.union(comp_bazr)
    all_analized_symbols = models.Company.objects.filter(id__in=comp_analiz).order_by('category__title')

    category_list = all_analized_symbols.values('category__id').annotate(dcount=Count('category')).distinct()
    categories = []
    for cat in category_list:
        cat_itm = get_object_or_404(models.Category, pk=cat['category__id'])
        symbols = all_analized_symbols.filter(category__id=cat_itm.id)
        categories.append({
            'category': cat_itm,
            'symbols': symbols,
        })

    len2 = int(len(categories)/4)
    cat_1 = categories[:len2]
    cat_2 = categories[len2:len2*2]
    cat_3 = categories[len2*2:len2*3]
    cat_4 = categories[len2*3:]
    cats = []
    cats.append(cat_1)
    cats.append(cat_2)
    cats.append(cat_3)
    cats.append(cat_4)
    return render(request, 'bourseapp/symbols/symbols_analyzed.html', {
        'categories': cats,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
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

    return render(request, 'bourseapp/news/new_list.html', {
        'newss': news,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, user=request.user)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = User.objects.get(id=request.user.id)  # use your own profile here
            cat = str(request.POST.get('category'))
            comp = str(request.POST.get('company'))
            if (cat != 'None'):
                candidate.category = models.Category.objects.get(
                    id=request.POST.get('category'))  # use your own profile here
            if (comp != 'None'):
                candidate.company = models.Company.objects.get(
                    id=request.POST.get('company'))  # use your own profile here

            candidate.save()
            return render(request, 'bourseapp/news/new_list.html')
    else:
        form = NewsForm(user=request.user)
    category = request.GET.get('category')
    company = request.GET.get('company')
    return render(request, 'bourseapp/news/news-create.html', {
        'form': form,
        'category': category,
        'company': company,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
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
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def webinar_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    webinar = models.Webinar.objects.filter(Q(company__symbol__icontains=search)
                                                | Q(createAt__icontains=search)
                                                | Q(description__icontains=search)
                                                )
    paginator = Paginator(webinar, page_size)
    try:
        webinar = paginator.page(page)
    except PageNotAnInteger:
        webinar = paginator.page(1)
    except EmptyPage:
        webinar = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/webinars/webinar_list.html', {
        'webinar': webinar,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def bazaar_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    bazaar = models.Bazaar.objects.filter(Q(company__symbol__icontains=search)
                                                | Q(createAt__icontains=search)
                                                | Q(description__icontains=search)
                                                )
    paginator = Paginator(bazaar, page_size)
    try:
        bazaar = paginator.page(page)
    except PageNotAnInteger:
        bazaar = paginator.page(1)
    except EmptyPage:
        bazaar = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/bazaar_list.html', {
        'bazaar': bazaar,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
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
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def tutorial_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    tutorial = models.Tutorial.objects.filter(Q(title__icontains=search)
                                              | Q(createAt__icontains=search)
                                              | Q(description__icontains=search)
                                              )
    paginator = Paginator(tutorial, page_size)
    try:
        tutorial = paginator.page(page)
    except PageNotAnInteger:
        tutorial = paginator.page(1)
    except EmptyPage:
        tutorial = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/tutorials/tutorial_list.html', {
        'tutorials': tutorial,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
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

    news = models.News.objects.filter(category=category_id)

    return render(request, 'bourseapp/category_detail.html', {
        'category': category,
        'companies': companies,
        'news': news,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def company_detail(request, company_id):
    company = get_object_or_404(models.Company, pk=company_id)
    news = models.News.objects.filter(company=company.id)
    technicals = models.Technical.objects.filter(company=company.id).exclude(user__username='d_abedi')
    fundamental = models.Fundamental.objects.filter(company=company.id)
    technicals_watch = models.Technical.objects.filter(company=company.id).filter(user__username='d_abedi')
    return render(request, 'bourseapp/compay_detail.html', {
        'company': company,
        'news': news,
        'technicals': technicals,
        'fundamentals': fundamental,
        'technicals_watch': technicals_watch,
        'tutorialCategory': tutorialCategory,
    })


@user_passes_test(lambda u: u.is_superuser)
def company_technical_view(request, company_id):
    company = get_object_or_404(models.Company, pk=company_id)
    technicals_watch = models.Technical.objects.filter(company=company.id)#.filter(user__username='d_abedi')
    return render(request, 'bourseapp/company_technical_view.html', {
        'company': company,
        'technicals_watch': technicals_watch,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
# @login_required
def news_detail(request, news_id):
    news = get_object_or_404(models.News, pk=news_id)
    return render(request, 'bourseapp/news/news_detail.html', {
        'news': news,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


@user_passes_test(lambda u: u.is_superuser)
def news_approve(request, news_id):
    news = get_object_or_404(models.News, pk=news_id)
    news.isApproved = True
    news.save()
    return HttpResponse("news approved")


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def technical_detail(request, technical_id):
    technical = get_object_or_404(models.Technical, pk=technical_id)
    return render(request, 'bourseapp/technical_detail.html', {
        'technical': technical,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def webinar_detail(request, webinar_id):
    webinar = get_object_or_404(models.Webinar, pk=webinar_id)
    return render(request, 'bourseapp/webinars/webinar_detail.html', {
        'webinar': webinar,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def bazaar_detail(request, bazaar_id):
    bazaar = get_object_or_404(models.Bazaar, pk=bazaar_id)
    return render(request, 'bourseapp/bazaar_detail.html', {
        'bazaar': bazaar,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def fundamental_detail(request, fundamental_id):
    fundamental = get_object_or_404(models.Fundamental, pk=fundamental_id)
    return render(request, 'bourseapp/fundamental_detail.html', {
        'fundamental': fundamental,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def tutorial_detail(request, tutorial_id):
    tutorial = get_object_or_404(models.Tutorial, pk=tutorial_id)
    return render(request, 'bourseapp/tutorials/tutorial_detail.html', {
        'tutorial': tutorial,
        'url': request.path,
        'tutorialCategory': tutorialCategory,
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


@user_passes_test(lambda u: u.is_superuser)
# @login_required
def message_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    messages = models.Message.objects.filter(Q(title__icontains=search)
                                             | Q(createAt__icontains=search)
                                             | Q(isShow__icontains=search)
                                             )
    paginator = Paginator(messages, page_size)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return render(request, 'bourseapp/message_list.html', {
        'messages': messages,
        'search': search,
        'page_size': page_size,
        'tutorialCategory': tutorialCategory,
    })


def tutorial_category(request, tutorialCategory_id):
    tutorialCat = get_object_or_404(models.TutorialCategory, pk=tutorialCategory_id)
    tutorialSubCat = models.TutorialSubCategory.objects.filter(category=tutorialCategory_id)
    return render(request, 'bourseapp/tutorials/tutorialCategory.html', {
        'tutorialCat': tutorialCat,
        'tutorialSubCat': tutorialSubCat,
        # 'url': request.path,
        'tutorialCategory': tutorialCategory,
    })


def tutorial_subCategory(request, tutorialSubCategory_id):
    tutorialSubCat = get_object_or_404(models.TutorialSubCategory, pk=tutorialSubCategory_id)
    tutorials = models.Tutorial.objects.filter(subCategory=tutorialSubCategory_id)
    return render(request, 'bourseapp/tutorials/tutorial_subCat_list.html', {
        'tutorials': tutorials,
        'tutorialSubCat': tutorialSubCat,
        'tutorialCategory': tutorialCategory,
    })