# Generated by Django 5.1.1 on 2024-12-15 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_lostitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='founditem',
            name='user',
            field=models.ForeignKey(db_column='id_user', default='1', on_delete=django.db.models.deletion.CASCADE, related_name='item_found', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lostitem',
            name='user',
            field=models.ForeignKey(db_column='id_user', default='1', on_delete=django.db.models.deletion.CASCADE, related_name='item_lost', to=settings.AUTH_USER_MODEL),
        ),
    ]
