from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from django.shortcuts import redirect

from . import models


@admin.register(models.Category)
class CategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:category-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:category-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:category-list')


@admin.register(models.Company)
class CompanyAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:company-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:company-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:company-list')


@admin.register(models.News)
class NewsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:news-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:news-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:news-list')


# admin.site.register(models.Category)
admin.site.register(models.Fundamental)
admin.site.register(models.Targets)
admin.site.register(models.Technical)
