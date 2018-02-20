# Generated by Django 2.0.2 on 2018-02-20 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='键名')),
                ('value', models.TextField(verbose_name='键值')),
                ('autoload', models.CharField(blank=True, choices=[('yes', '是'), ('no', '否')], default='yes', max_length=20, verbose_name='自动载入')),
            ],
            options={
                'verbose_name': '站点配置',
                'verbose_name_plural': '站点配置',
            },
        ),
        migrations.CreateModel(
            name='UserMeta',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='键名')),
                ('value', models.TextField(blank=True, default='', verbose_name='键值')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户信息')),
            ],
            options={
                'verbose_name': '用户元数据',
                'verbose_name_plural': '用户元数据',
            },
        ),
    ]
