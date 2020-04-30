from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
# from meta.models import ModelMeta


def scramble_uploaded_filename(instance, filename):
    extention = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extention)


class Category(models.Model): #ModelMeta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    # _metadata = {
    #     'title': 'title',
    #     'description': 'description',
    #     'image': 'get_meta_image',
    # }

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:category-detail", kwargs={'category_id': self.pk})

    # def get_meta_image(self):
    #     if self.pic:
    #         return self.pic.url


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='گروه')
    symbol = models.CharField(max_length=120, null=True, blank=True, help_text='نماد')
    fullName = models.CharField(max_length=120, null=True, blank=True, help_text='نام شرکت')
    bourseType = models.CharField(max_length=120, null=True, blank=True, help_text='بازار بورس')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    tse = models.URLField(null=True, blank=True, help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:company-detail", kwargs={'company_id': self.pk})


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
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    tag = models.CharField(max_length=120, null=True, blank=True, help_text='تگ ها')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    isApproved = models.BooleanField(default=False, help_text='تایید خبر')
    isImportant = models.BooleanField(default=False, help_text='خبر مهم')
    shortDescription = models.TextField(max_length=200, null=True, blank=True, help_text='توضیحات کوتاه')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')


    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:news-detail", kwargs={'news_id': self.pk})


class Technical(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    video = models.FileField(upload_to='videos/', null=True, blank=True, help_text='فایل ویدیو')
    audio = models.FileField(upload_to='audio/', null=True, blank=True, help_text='فایل صوتی')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:technical-detail", kwargs={'technical_id': self.pk})


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='فرستنده')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='گیرنده')
    createAt = models.DateTimeField(default=timezone.now, help_text='تاریخ ایجاد')
    isSeen = models.BooleanField(default=False, help_text='مشاهده شده')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return str(self.sender)

    @property
    def owner(self):
        return self.sender


class Webinar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:webinar-detail", kwargs={'webinar_id': self.pk})


class Fundamental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:fundamental-detail", kwargs={'fundamental_id': self.pk})


class Bazaar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:bazaar-detail", kwargs={'bazaar_id': self.pk})


TIME_FRAME_CHOICES = (
    ('0', "1 دقیقه"),
    ('1', "5 دقیقه"),
    ('2', "15 دقیقه"),
    ('3', "30 دقیقه"),
    ('4', "45 دقیقه"),
    ('5', "۱ ساعت"),
    ('6', "4 ساعت"),
    ('7', "1 روز"),
    ('8', "1 هفته"),
    ('9', "1 ماه"),
)
class Chart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    timeFrame = models.CharField(max_length=20, help_text='تایم فریم', choices=TIME_FRAME_CHOICES, default='7')
    data = models.FileField('uploaded chart file', null=True, blank=True, help_text='فایل csv چارت نماد')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class TutorialCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


CATEGORY_LEVEL_CHOICES = (
    ('0', "مقدماتی"),
    ('1', "پیشرفته"),
)
class TutorialSubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='دسته بندی')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    categoryLevel = models.CharField(max_length=20, help_text='سطح آموزش', choices=CATEGORY_LEVEL_CHOICES,
                                default='0')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class Tutorial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    file = models.FileField('uploaded file', null=True, blank=True, help_text='فایل')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    # category = models.CharField(max_length=120, null=True, blank=True, help_text='دسته آموزش', choices=CATEGORY_CHOICES,
    #                             default='تحلیل بازار')
    subCategory = models.ForeignKey(TutorialSubCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='زیر دسته بندی')
    externalLink = models.URLField(null=True, blank=True, help_text='لینک آموزش')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:tutorial-detail", kwargs={'tutorial_id': self.pk})


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    isShow = models.BooleanField(default=False, help_text='نمایش برای کاربران')
    title = models.TextField(max_length=3000, null=True, blank=True, help_text='پیام')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user
