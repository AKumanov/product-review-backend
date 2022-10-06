import datetime

from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField


# Create your models here.


class Company(models.Model):
    __COMPANY_MAX_NAME = 255
    name = models.CharField(
        max_length=__COMPANY_MAX_NAME
    )
    url = models.TextField()

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    __PRODUCT_SIZE_MAX_NAME = 255
    name = models.CharField(
        max_length=__PRODUCT_SIZE_MAX_NAME
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    __CAT_MAX_NAME = 255
    name = models.CharField(
        max_length=__CAT_MAX_NAME
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    __PRODUCT_MAX_NAME = 255
    name = models.CharField(
        max_length=__PRODUCT_MAX_NAME
    )
    content = models.TextField()
    category = models.ManyToManyField(
        Category,
        related_name='products'
    )
    created = models.DateField(
        auto_now_add=True
    )
    updated = models.DateField(
        auto_now=True
    )
    image = models.ManyToManyField(
        'reviews.Image',
        related_name='products'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class ProductSite(models.Model):
    __PRODUCT_SITE_MAX_NAME = 255
    name = models.CharField(
        max_length=__PRODUCT_SITE_MAX_NAME
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sites',
        related_query_name='site'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='sites',
        related_query_name='site'
    )
    productsize = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        related_name='sites',
        related_query_name='site'
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    url = models.TextField()
    created = models.DateField(
        auto_now_add=True
    )
    updated = models.DateField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    __COMMENT_MAX_TITLE = 255
    title = models.CharField(
        max_length=__COMMENT_MAX_TITLE
    )
    content = models.TextField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment'
    )
    created = models.DateField(
        auto_now_add=True,
    )
    updated = models.DateField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class CustomerReportRecord(models.Model):
    time_raised = models.DateTimeField(
        default=datetime.datetime.now(),
        editable=False
    )
    reference = models.CharField(
        unique=True,
        max_length=20
    )
    description = models.TextField()


class Image(models.Model):
    __IMAGE_MAX_NAME = 255
    name = models.CharField(
        max_length=__IMAGE_MAX_NAME
    )
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
