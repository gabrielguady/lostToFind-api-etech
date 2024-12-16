from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from api_lost import settings
from core.managers import UserManager


class ModelBase(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        null=False,
        db_column='id',

    )
    date_created = models.DateTimeField(
        db_column='dt_created',
        auto_now_add=True,
        null=False,
    )
    date_modified = models.DateTimeField(
        db_column='dt_modified',
        auto_now=True,
        null=False,
    )

    class Meta:
        abstract = True
        managed = True


class Category(ModelBase):
    name = models.CharField(
        db_column='tx_name',
        null=False,
    )

    def __str__(self):
        return self.name


class FileImageItem(ModelBase):
    filename = models.CharField(
        db_column='tx_file_name',
        null=False,
        blank=False,
        max_length=255,
    )
    remote_name = models.CharField(
        db_column='tx_remote_name',
        max_length=1024,
        null=False,
        blank=False,
    )
    lost_item = models.ForeignKey(
        to='LostItem',
        on_delete=models.CASCADE,
        db_column='id_lost_item',
        null=True,
        blank=True,
        related_name='file_image_items'
    )
    found_item = models.ForeignKey(
        to='FoundItem',
        on_delete=models.CASCADE,
        db_column='id_found_item',
        null=True,
        blank=True,
        related_name='file_image_items'
    )

    class Meta:
        db_table = 'file_image_item'
        managed = True


class LostItem(ModelBase):
    title = models.CharField(
        db_column='tx_title',
        null=False,
        max_length=100,
    )
    last_seen_details = models.TextField(
        db_column='tx_description',
        null=False,
        max_length=250,
    )
    reward = models.FloatField(
        db_column='nb_price',
        null=False,
    )
    date_lost = models.DateTimeField(
        db_column='dt_lost',
        null=False,
    )
    is_resolved = models.BooleanField(
        db_column='cs_resolved',
        default=False,
        null=False,
    )
    city = models.CharField(
        db_column='tx_city',
        null=False,
        max_length=100,
        default='brasil'
    )
    category = models.ForeignKey(
        Category,
        db_column='id_category',
        null=True,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='id_user',
        on_delete=models.CASCADE,
        null=False,
        default='1',
        related_name = 'item_lost'
    )

    class Meta:
        db_table = 'item_lost'
        managed = True


class FoundItem(ModelBase):
    title = models.CharField(
        db_column='tx_title',
        null=False,
        max_length=100,
    )
    description = models.TextField(
        db_column='tx_description',
        null=False,
        max_length=250,
    )
    date_found = models.DateTimeField(
        db_column='dt_found',
        null=False,
    )
    is_resolved = models.BooleanField(
        db_column='cs_resolved',
        default=False,
        null=False,
    )
    city = models.CharField(
        db_column='tx_city',
        null=False,
        max_length=100,
        default='brasil'
    )
    category = models.ForeignKey(
        Category,
        db_column='id_category',
        null=True,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='id_user',
        on_delete=models.CASCADE,
        null=False,
        default='1',
        related_name='item_found'
    )

    class Meta:
        db_table = 'item_found'
        managed = True


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_column='tx_username',
        null=False,
        max_length=64,
        unique=True,
    )
    password = models.CharField(
        db_column='tx_password',
        null=False,
        max_length=104,
    )
    email = models.CharField(
        db_column='tx_email',
        null=True,
        max_length=256,
    )
    last_login = models.DateTimeField(
        db_column='dt_last_login',
        null=True,
    )
    is_active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True,
    )
    is_superuser = models.BooleanField(
        db_column='cs_superuser',
        null=True,
        default=False,
    )
    is_staff = models.BooleanField(
        db_column='cs_staff',
        null=True,
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

