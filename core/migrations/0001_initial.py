# Generated by Django 5.1.1 on 2024-12-15 06:52

import core.managers
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='dt_created')),
                ('date_modified', models.DateTimeField(auto_now=True, db_column='dt_modified')),
                ('name', models.CharField(db_column='tx_name')),
            ],
            options={
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_column='tx_username', max_length=64, unique=True)),
                ('password', models.CharField(db_column='tx_password', max_length=104)),
                ('email', models.CharField(db_column='tx_email', max_length=256, null=True)),
                ('last_login', models.DateTimeField(db_column='dt_last_login', null=True)),
                ('is_active', models.BooleanField(db_column='cs_active', default=True)),
                ('is_superuser', models.BooleanField(db_column='cs_superuser', default=False, null=True)),
                ('is_staff', models.BooleanField(db_column='cs_staff', default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', core.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FoundItem',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='dt_created')),
                ('date_modified', models.DateTimeField(auto_now=True, db_column='dt_modified')),
                ('title', models.CharField(db_column='tx_title', max_length=100)),
                ('description', models.TextField(db_column='tx_description', max_length=250)),
                ('date_found', models.DateTimeField(db_column='dt_found')),
                ('is_resolved', models.BooleanField(db_column='cs_resolved', default=False)),
                ('city', models.CharField(db_column='tx_city', default='brasil', max_length=100)),
                ('category', models.ForeignKey(db_column='id_category', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('user', models.ForeignKey(db_column='id_user', default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'item_found',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LostItem',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='dt_created')),
                ('date_modified', models.DateTimeField(auto_now=True, db_column='dt_modified')),
                ('title', models.CharField(db_column='tx_title', max_length=100)),
                ('last_seen_details', models.TextField(db_column='tx_description', max_length=250)),
                ('reward', models.FloatField(db_column='nb_price')),
                ('date_lost', models.DateTimeField(db_column='dt_lost')),
                ('is_resolved', models.BooleanField(db_column='cs_resolved', default=False)),
                ('city', models.CharField(db_column='tx_city', default='brasil', max_length=100)),
                ('category', models.ForeignKey(db_column='id_category', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.category')),
                ('user', models.ForeignKey(db_column='id_user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'item_lost',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FileImageItem',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_column='dt_created')),
                ('date_modified', models.DateTimeField(auto_now=True, db_column='dt_modified')),
                ('filename', models.CharField(db_column='tx_file_name', max_length=255)),
                ('remote_name', models.CharField(db_column='tx_remote_name', max_length=1024)),
                ('found_item', models.ForeignKey(blank=True, db_column='id_found_item', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_image_items', to='core.founditem')),
                ('lost_item', models.ForeignKey(blank=True, db_column='id_lost_item', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_image_items', to='core.lostitem')),
            ],
            options={
                'db_table': 'file_image_item',
                'managed': True,
            },
        ),
    ]
