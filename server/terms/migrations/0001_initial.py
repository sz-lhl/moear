# Generated by Django 2.0.2 on 2018-02-20 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationships',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post', verbose_name='文章数据')),
            ],
            options={
                'verbose_name': '分类关系',
                'verbose_name_plural': '分类关系',
            },
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('taxonomy_type', models.CharField(max_length=32, verbose_name='分类类型')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('count', models.BigIntegerField(blank=True, default=0, verbose_name='文章计数')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='terms.Taxonomy', verbose_name='父分类')),
            ],
            options={
                'verbose_name': '分类数据',
                'verbose_name_plural': '分类数据',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='术语名')),
                ('slug', models.CharField(max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': '术语数据',
                'verbose_name_plural': '术语数据',
            },
        ),
        migrations.AddField(
            model_name='taxonomy',
            name='term',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='terms.Term', verbose_name='术语'),
        ),
        migrations.AddField(
            model_name='relationships',
            name='taxonomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terms.Taxonomy', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='relationships',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterUniqueTogether(
            name='relationships',
            unique_together={('post', 'taxonomy', 'user')},
        ),
    ]
