from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid
from ckeditor_uploader.fields import RichTextUploadingField


def scramble_uploaded_filename(instance, filename):
    extention = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extention)


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='تصویر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='گروه')
    symbol = models.CharField(max_length=120, null=True, blank=True, help_text='نماد')
    fullName = models.CharField(max_length=120, null=True, blank=True, help_text='نام شرکت')
    bourseType = models.CharField(max_length=120, null=True, blank=True, help_text='بازار بورس')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='تصویر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    tse = models.URLField(null=True, blank=True, help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.symbol

    @property
    def owner(self):
        return self.user


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE,
                                 help_text='در صورت اختصاص خبر برای گروه انتخاب شود')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                help_text='در صورت اختصاص خبر برای نماد انتخاب شود')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    reference = models.CharField(max_length=120, null=True, blank=True, help_text='مرجع')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='تصویر')
    tag = models.CharField(max_length=120, null=True, blank=True, help_text='تگ ها')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class Technical(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class Fundamental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


CATEGORY_CHOICES = (
    ("تحلیل بنیادی", "تحلیل بنیادی"),
    ("تحلیل تکنیکال", "تحلیل تکنیکال"),
    ("تحلیل بازار", "تحلیل بازار"),
)


class Tutorial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    file = models.FileField('uploaded file', null=True, blank=True, upload_to=scramble_uploaded_filename,
                            help_text='فایل')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    category = models.CharField(max_length=120, null=True, blank=True, help_text='دسته آموزش', choices=CATEGORY_CHOICES,
                                default='تحلیل بازار')
    externalLink = models.URLField(null=True, blank=True, help_text='لینک آموزش')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user
